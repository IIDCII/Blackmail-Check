import os
import sqlite3
from groq import Groq
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_severity(db_name='images.db'):
    """
    Initialize all the records' severity to 'PENDING' in the database.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Set all severity to 'PENDING' initially
    cursor.execute("UPDATE master_table SET severity='PENDING', description=NULL")
    connection.commit()
    connection.close()

    logging.info("All file severities set to 'PENDING'.")

def cleanup_missing_files(db_name='images.db'):
    """
    Remove database entries for files that no longer exist on the filesystem.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    # Get all file paths from database
    cursor.execute("SELECT id, file_path FROM master_table")
    rows = cursor.fetchall()
    
    removed_count = 0
    for row_id, file_path in rows:
        if not os.path.exists(file_path):
            cursor.execute("DELETE FROM master_table WHERE id=?", (row_id,))
            removed_count += 1
            logging.info(f"Removed missing file from database: {file_path}")
    
    connection.commit()
    connection.close()
    
    if removed_count > 0:
        logging.info(f"Cleaned up {removed_count} missing files from database")

def generate_ratings(db_name='images.db'):
    """
    Process all images, classify them, and update their severity and description.
    """
    # First clean up any missing files
    cleanup_missing_files(db_name)
    
    # Connect to the database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Select all files with PENDING status
    cursor.execute("SELECT file_path FROM master_table WHERE severity='PENDING'")
    rows = cursor.fetchall()

    if not rows:
        logging.info("No pending files to process")
        connection.close()
        return

    # Setup Groq client
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logging.error("GROQ_API_KEY environment variable not set")
        connection.close()
        return
        
    client = Groq(api_key=api_key)

    for row in rows:
        relative_file_path = row[0]

        # Double-check if the file exists
        if os.path.exists(relative_file_path):
            try:
                # Run the image through the LLM and get the classification
                severity, description = return_rating(relative_file_path, client)

                # If valid results, update the database
                if severity is not None and description:
                    cursor.execute("UPDATE master_table SET severity=?, description=? WHERE file_path=?", 
                                   (severity, description, relative_file_path))
                    logging.info(f"Updated {relative_file_path} with severity {severity}")
                else:
                    logging.warning(f"Failed to classify {relative_file_path}. Results were invalid.")

            except Exception as e:
                logging.error(f"Error processing {relative_file_path}: {e}")
                # Mark as failed instead of leaving as pending
                cursor.execute("UPDATE master_table SET severity=?, description=? WHERE file_path=?", 
                               ("FAILED", f"Error: {str(e)}", relative_file_path))
        else:
            logging.warning(f"File '{relative_file_path}' not found during processing.")

    # Commit changes and close the connection
    connection.commit()
    connection.close()

def return_rating(file_path, client) -> tuple[str, str]:
    """
    Classifies the image file at the provided path as SFW (0) or NSFW (1).
    It returns the classification (0 or 1) and an explanation (description).
    """
    try:
        # Open and encode the image to base64
        with open(file_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Groq API request to classify the image
        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # Current Groq vision model
            max_completion_tokens=200,
            temperature=1,
            top_p=1,
            stream=False,
            messages=[
                {
                    "role": "system",
                    "content": "You are a content moderation AI for a cybersecurity tool. Classify images as either 'SFW' (safe for work) or 'NSFW' (not safe for work). Respond with just the classification followed by a brief explanation. Format: 'SFW: [reason]' or 'NSFW: [reason]'"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please classify this image as SFW or NSFW and provide a brief explanation."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ]
        )

        # Parse the model's response to get the severity (0 or 1) and explanation
        message_content = chat_completion.choices[0].message.content

        # Debug: Log the raw message content to check what the model returns
        logging.info(f"Model response: {message_content}")

        # Initialize severity and description
        severity = None
        description = message_content.strip()

        # Parse the response - look for SFW or NSFW at the beginning
        content_upper = message_content.upper()
        if content_upper.startswith("SFW"):
            severity = "SFW"
        elif content_upper.startswith("NSFW"):
            severity = "NSFW"
        elif "SFW" in content_upper and "NSFW" not in content_upper:
            severity = "SFW"
        elif "NSFW" in content_upper:
            severity = "NSFW"
        else:
            # Try to detect based on content keywords
            safe_keywords = ["safe", "appropriate", "family", "clean", "innocent"]
            unsafe_keywords = ["inappropriate", "explicit", "sexual", "nude", "adult"]
            
            content_lower = message_content.lower()
            if any(keyword in content_lower for keyword in unsafe_keywords):
                severity = "NSFW"
            elif any(keyword in content_lower for keyword in safe_keywords):
                severity = "SFW"

        # If no classification was found, handle error gracefully
        if severity is None:
            logging.warning(f"Could not determine classification from response: {message_content}")
            return "UNKNOWN", message_content

        # Clean the description
        description = clean_description(description)

        return severity, description

    except Exception as e:
        logging.error(f"Error processing image {file_path}: {e}")
        return None, None

def clean_description(description: str) -> str:

    # Further clean the description (e.g., remove leading spaces, extra punctuation, etc.)
    description = description.strip()
    
    return description