from flask import Flask
from blackmail_file_scanner import display

app = Flask(__name__)

@app.route('/')
def index():
    return display()

if __name__ == '__main__':
    app.run(debug=True)