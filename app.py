from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from scraper import find_exposed_pii
from hibp import check_breaches

load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = os.getenv("DEBUG", "False") == "True"

@app.route("/hibp", methods=["POST"])
def hibp():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    results = check_breaches(email)
    return jsonify(results)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    findings = find_exposed_pii(query)
    return jsonify(findings)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(debug=True)

