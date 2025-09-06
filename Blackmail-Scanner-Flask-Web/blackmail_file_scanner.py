import sqlite3
import pandas as pd
import os

# Use this to scan the directory
def scan_directory_to_db(path="C:/Users/ADMIN/PycharmProjects", db_name='files.db', table_name='files'):
    records = []
    for root, _, files in os.walk(path):
        for f in files:
            filepath = os.path.join(root, f)
            size = os.path.getsize(filepath)
            records.append((root, f, size))

    df = pd.DataFrame(records, columns = ['filepath', 'filename', 'size_bytes'])

    with sqlite3.connect(db_name) as connection:
        df.to_sql(table_name, connection, if_exists='replace', index=False)

    print(f"Inserted {len(df)} files into {db_name}:{table_name}")
    return df

# Use this to serve the table to the web server
def display():
    with sqlite3.connect('files.db') as connection:
        select_query = "SELECT * FROM files;"
        df = pd.read_sql_query(select_query, connection)
    # Return as HTML table
    return df.to_html()