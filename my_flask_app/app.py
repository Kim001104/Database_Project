from flask import Flask, render_template, request
from database import get_db, init_db

app = Flask(__name__)

@app.before_first_request
def initialize():
    init_db()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)