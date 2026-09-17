from flask import Flask, jsonify, render_template, request
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["flask_database"]
collection = db["students"]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            name = request.form["name"]
            course = request.form["course"]

            collection.insert_one({
                "name": name,
                "course": course
            })

            return "Data submitted successfully"

        except Exception as error:
            return f"Error: {error}"

    return render_template("index.html")


@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)