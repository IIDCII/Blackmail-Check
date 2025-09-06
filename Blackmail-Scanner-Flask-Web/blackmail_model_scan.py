from groq import Groq
import os
import sqlite3


def generate_ratings(db_name='images.db'):
    # loop through the db
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT file_path FROM master_table WHERE severity='PENDING'")
    rows = cursor.fetchall()
    
    # setup Groq client
    client = Groq(
        api_key= os.environ.get("GROQ_API_KEY")
    )

    for row in rows:
        file_path = row[0]
        rating = return_rating(file_path, client)[0]
        severity = return_rating(file_path, client)[1:]
        
        # update the db
        cursor.execute("UPDATE master_table SET severity=?, description=? WHERE file_path=?", (severity, rating, file_path))

    return None


def return_rating(file_path, client) -> list[str,str]:
    # just working with images for the time being



    # return rating using groq
    chat_completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        max_completion_tokens=512,
        temperature=1,  
        top_p=1,
        stream = False,
        stop = None,
        messages = [
            {
                "role": "system",
                "content": "You are a cybersecurity expert. You will be given a file path. You will read the file and return a severity rating (CRITICAL, HIGH, MEDIUM, LOW, NONE) and a short description of why you gave that rating. If the file is empty or cannot be read, return NONE as the severity and an empty description. You have to return the first token as the severity and the rest as the description split by a newline."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type":"image_url",
                        "image_url": {"url":f"data:image/jpeg;base64,{open(file_path, 'rb').read().encode('base64')}"}
                    }
                ]
            },
            {
                "role": "user",
                "content":"Here is the file path"
            }
        ]
    )
    print (chat_completion.choices[0].message.content)
    
    return chat_completion.choices[0].message.content