from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get your HIBP API key from the environment
HIBP_API_KEY = os.getenv("HIBP_API_KEY")

@app.route('/')
def hello():
    return 'Hello, world! The Flask app is running.'

@app.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Missing email"}), 400

    headers = {
        "hibp-api-key": HIBP_API_KEY,
        "user-agent": "FlaskSpikeApp"
    }

    response = requests.get(
        f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
        headers=headers,
        params={"truncateResponse": "false"}
    )

    if response.status_code == 200:
        return jsonify({"breaches": response.json()}), 200
    elif response.status_code == 404:
        return jsonify({"message": "No breaches found for this email."}), 200
    else:
        return jsonify({
            "error": "HIBP API request failed",
            "status": response.status_code
        }), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
