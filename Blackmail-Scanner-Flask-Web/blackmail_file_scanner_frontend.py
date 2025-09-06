from flask import Flask
from blackmail_file_scanner import display, scan_directory_to_db
from blackmail_model_scan import generate_ratings

app = Flask(__name__)

@app.route('/')
def index():
    # Display the table data on the webpage
    return display()

if __name__ == '__main__':
    # Step 1: Scan the directory and add file paths to the database
    scan_directory_to_db()

    # Step 2: Process the files and classify them
    generate_ratings()

    # Step 3: Run the Flask app
    app.run(debug=True)