import sqlite3
import pandas as pd
import os

# Use this to scan the directory
def scan_directory_to_db(path="mock_data", db_name='images.db'):
    if not os.path.exists(path):
        raise ValueError(f"Path does not exist")
    
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        create_table_command = """
        CREATE TABLE IF NOT EXISTS master_table (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL UNIQUE,
            severity TEXT DEFAULT 'PENDING',
            description TEXT
        );"""
        cursor.execute(create_table_command)

        files_to_insert = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                # Get the absolute path to ensure uniqueness
                # get the relative path along with the filename
                path = os.path.relpath(root, path)
                full_path = os.path.join(path, filename)
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

# Use this to serve the table to the web server
def display():
    with sqlite3.connect('images.db') as connection:
        select_query = "SELECT * FROM master_table;"
        df = pd.read_sql_query(select_query, connection)
    
    # Return as HTML table
    return df.to_html()