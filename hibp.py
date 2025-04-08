import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HIBP_API_KEY")

def check_breaches(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "PIIPrivacyTool"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            return {"breaches": [], "message": "No breaches found."}
        elif response.status_code == 200:
            return {"breaches": response.json()}
        else:
            return {"error": f"Unexpected status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

