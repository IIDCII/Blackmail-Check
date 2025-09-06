"""
For the actual implementation, we will be taking the data directly from the google drive folder
and storing that in a db with the same table structure as before.
"""

import sqlite3
import os
from groq import Groq

def populate_files_to_db(directory_path, db_name='store_master_table.db'):
    print
    if not os.path.isdir(directory_path):
        print("Error: Directory not found")
        return 

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        create_table_command = """
        CREATE TABLE IF NOT EXISTS master_table (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL UNIQUE,
            severity TEXT NOT NULL,
            description TEXT
        );"""
        cursor.execute(create_table_command)

        files_to_insert = []
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                # Get the absolute path to ensure uniqueness
                full_path = os.path.abspath(os.path.join(root, filename))
                # Prepare a tuple for insertion with default values
                # (file_path, severity, description)
                files_to_insert.append((full_path, 'PENDING', None))

        if files_to_insert:
            insert_query = "INSERT OR IGNORE INTO master_table (file_path, severity, description) VALUES (?, ?, ?)"
            cursor.executemany(insert_query, files_to_insert)
            print("Database is up to date.")
        else:
            print("No new files found to add.")

        connection.commit()
        connection.close()
        print("Successfully populated file paths into")

    except sqlite3.Error as e:
        print("Database error")
    except Exception as e:
        print("An error occurred")


def scan_directory(directory_path):
    print("Scanning directory..")
    return
    # loop through the db
    connection = sqlite3.connect('store_master_table.db')
    cursor = connection.cursor()
    cursor.execute("SELECT file_path FROM master_table WHERE severity='PENDING'")
    rows = cursor.fetchall()
    
    # setup Groq client
    client = Groq(
        api_key= os.environ.get("GROQ_API_KEY")
    )

    for row in rows:
        file_path = row[0]
        rating = return_rating(file_path)[0]
        severity = return_rating(file_path)[1]
        
        # update the db
        cursor.execute("UPDATE master_table SET severity=?, description=? WHERE file_path=?", (severity, rating, file_path))

    return None

def return_rating(file_path, client) -> list[str,str]:
    # check the file type (pdf,md,txt,jpg,jpeg,png,etc)

    # return rating using groq
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=200,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity expert. You will be given a file path. You will read the file and return a severity rating (HIGH RISK, LOW RISK, NONE) and a short description of why you gave that rating. If the file is empty or cannot be read, return NONE as the severity and an empty description."
            },
            {
                "role": "user",
                "content": f"Read the file at this path: {file_path} and return a severity rating (HIGH RISK, LOW RISK, NONE) and a short description of why you gave that rating. If the file is empty or cannot be read, return NONE as the severity and an empty description."
            }
        ],
    )

    return chat_completion.choices[0].message.content.split("\n")



if __name__ == '__main__':
    directory_to_scan = 'data'
    
    populate_files_to_db(directory_to_scan)

    print ("Scanning for vulnerabilities...")
    scan_directory(directory_to_scan)
    print ("Scan complete.")
    
    # show db for demonstration
    connection = sqlite3.connect('store_master_table.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM master_table")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    connection.close()