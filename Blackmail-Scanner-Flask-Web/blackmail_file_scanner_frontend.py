from flask import Flask, render_template
import sqlite3
import pandas as pd
import os
from blackmail_model_scan import generate_ratings

app = Flask(__name__)

# Replicate the functions from blackmail_file_scanner.py
def scan_directory_to_db(path="mock_data", db_name='images.db'):
    if not os.path.exists(path):
        print(f"Creating mock_data directory...")
        os.makedirs(path, exist_ok=True)
        return
    
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
                # Get relative path from mock_data
                rel_path = os.path.relpath(os.path.join(root, filename), start=os.getcwd())
                files_to_insert.append((rel_path, 'PENDING', None))

        if files_to_insert:
            insert_query = "INSERT OR IGNORE INTO master_table (file_path, severity, description) VALUES (?, ?, ?)"
            cursor.executemany(insert_query, files_to_insert)
            print(f"Added {cursor.rowcount} new files to database.")
        else:
            print("No files found to add.")

        connection.commit()
        connection.close()
        print("Database updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def display():
    try:
        with sqlite3.connect('images.db') as connection:
            select_query = "SELECT * FROM master_table;"
            df = pd.read_sql_query(select_query, connection)
        
        if df.empty:
            return render_template('index.html', table_data="<p>No files found in database. Please add some files to the mock_data directory.</p>")
        
        # Convert severity numbers to readable text and handle all status types
        df['severity'] = df['severity'].replace({
            0: 'SFW', 
            1: 'NSFW', 
            'PENDING': 'PENDING',
            'FAILED': 'FAILED',
            'UNKNOWN': 'UNKNOWN'
        })
        
        # Return as HTML table with styling
        table_html = df.to_html(classes='table table-striped table-bordered', table_id='results-table', escape=False)
        return render_template('index.html', table_data=table_html)
    
    except Exception as e:
        return render_template('index.html', table_data=f"<p>Error loading data: {e}</p>")


@app.route('/')
def index():
    # Display the table data on the webpage
    return display()

@app.route('/scan')
def scan():
    # Trigger a new scan
    scan_directory_to_db()
    
    # Check if GROQ_API_KEY is available
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return """
        <div style='padding: 20px; font-family: Arial;'>
            <h2>⚠️ API Key Missing</h2>
            <p>GROQ_API_KEY environment variable is not set.</p>
            <p>The scanner has updated the file database but cannot run AI classification.</p>
            <p><strong>To enable AI scanning:</strong></p>
            <ol>
                <li>Get a GROQ API key from <a href="https://console.groq.com/" target="_blank">console.groq.com</a></li>
                <li>Set the GROQ_API_KEY environment variable</li>
                <li>Run the scan again</li>
            </ol>
            <p><a href="/" class="btn">← Back to Results</a></p>
        </div>
        """
    
    try:
        generate_ratings()
        return """
        <div style='padding: 20px; font-family: Arial;'>
            <h2>✅ Scan Completed!</h2>
            <p>Files have been processed and classified.</p>
            <p><a href="/">← View Results</a></p>
        </div>
        """
    except Exception as e:
        return f"""
        <div style='padding: 20px; font-family: Arial;'>
            <h2>❌ Scan Failed</h2>
            <p>Error: {str(e)}</p>
            <p><a href="/">← Back to Results</a></p>
        </div>
        """

@app.route('/health')
def health_check():
    return {"status": "healthy", "service": "Blackmail Check Scanner"}

if __name__ == '__main__':
    # Step 1: Scan the directory and add file paths to the database
    scan_directory_to_db()

    # Step 2: Process the files and classify them (only in development)
    if os.environ.get('FLASK_ENV') != 'production':
        print("Processing files with AI model...")
        generate_ratings()

    # Step 3: Run the Flask app
    print("Starting Flask web server...")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)