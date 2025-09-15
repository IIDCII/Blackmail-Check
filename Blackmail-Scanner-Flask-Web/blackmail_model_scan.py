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

def generate_ratings(db_name='images.db'):
    """
    Process all images, classify them, and update their severity and description.
    """
    # Connect to the database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Select all files from the database (without filtering by severity)
    cursor.execute("SELECT file_path FROM master_table")
    rows = cursor.fetchall()

    # Setup Groq client
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    for row in rows:
        relative_file_path = row[0]

        # Check if the file exists
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
        else:
            logging.warning(f"File '{relative_file_path}' not found.")

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
            model="llama-3.2-11b-vision-preview",  # Specify model for image classification
            max_completion_tokens=200,
            temperature=1,
            top_p=1,
            stream=False,
            messages=[
                {
                    "role": "system",
                    "content": "You are a content moderation AI. You will classify images into SFW (0) or NSFW (1) categories."
                },
                {
                    "role": "user",
                    "content": [
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
        description = ""

        # Look for severity (SFW or NSFW) and clean up description
        if "SFW" in message_content.upper() or "0" in message_content:
            severity = "SFW"
            description = message_content
        elif "NSFW" in message_content.upper() or "1" in message_content:
            severity = "NSFW"
            description = message_content

        # If no classification was found, handle error gracefully
        if severity is None:
            logging.warning(f"Invalid response format: {message_content}")
            return None, None

        # Clean the description by removing unwanted phrases (e.g., 'I would classify this image as...')
        description = clean_description(description)

        return severity, description

    except Exception as e:
        logging.error(f"Error processing image {file_path}: {e}")
        return None, None

def clean_description(description: str) -> str:

    # Further clean the description (e.g., remove leading spaces, extra punctuation, etc.)
    description = description.strip()
    
    return description