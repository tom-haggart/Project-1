import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import re
import requests
from bs4 import BeautifulSoup

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def find_exposed_pii(query):
    results = []

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY
    }

    try:
        search = GoogleSearch(params)
        serp_results = search.get_dict()

        for result in serp_results.get("organic_results", []):
            url = result.get("link")
            if not url.startswith("http"):
                continue

            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()

                emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
                phones = re.findall(r"\b(?:\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}\b", text)

                if emails or phones:
                    results.append({
                        "url": url,
                        "emails": emails,
                        "phone_numbers": phones
                    })

            except Exception as e:
                results.append({"url": url, "error": str(e)})

    except Exception as e:
        return [{"error": f"SerpAPI search failed: {e}", "url": query}]

    return results

