# utils/safe_browsing.py

import requests
import os

API_KEY = os.environ.get("API_KEY")

def check_safe_browsing(url):
    try:
        # ❌ If no API key → don't fake safe
        if not API_KEY:
            return None  # unknown

        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

        payload = {
            "client": {
                "clientId": "phishing-detector",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        res = requests.post(api_url, json=payload)
        result = res.json()

        if "matches" in result:
            return False   # ❌ Dangerous
        else:
            return True    # ✅ Safe

    except Exception as e:
        print("Safe browsing error:", e)
        return None