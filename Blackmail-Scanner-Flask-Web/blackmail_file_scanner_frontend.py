from flask import Flask
from blackmail_file_scanner import display
from blackmail_file_scanner import scan_directory_to_db
from blackmail_model_scan import generate_ratings

app = Flask(__name__)

@app.route('/')
def index():
    return display()

if __name__ == '__main__':
    scan_directory_to_db()
    # bring this back in later
    # generate_ratings()
    app.run(debug=True)