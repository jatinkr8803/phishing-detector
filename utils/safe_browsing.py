import requests
import os

# 🔐 Secure API key from environment variable
API_KEY = os.environ.get("API_KEY")


def check_safe_browsing(url):
    try:
        # Check if API key exists
        if not API_KEY:
            return "Error"

        # Google Safe Browsing API endpoint
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

        # Request payload
        payload = {
            "client": {
                "clientId": "phishing-detector",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }

        # Send POST request
        response = requests.post(endpoint, json=payload)

        # Check response status
        if response.status_code != 200:
            return "Error"

        data = response.json()

        # Check if URL is flagged
        if "matches" in data:
            return "Blacklisted"
        else:
            return "Safe"

    except Exception as e:
        print("Safe Browsing Error:", e)
        return "Error"