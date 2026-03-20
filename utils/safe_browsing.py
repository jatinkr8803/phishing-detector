# utils/safe_browsing.py

import requests
import os

def check_safe_browsing(url):
    try:
        API_KEY = os.environ.get("API_KEY")

        # ❌ No API key
        if not API_KEY:
            return "Not Verified"

        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

        payload = {
            "client": {
                "clientId": "phishing-detector",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        res = requests.post(api_url, json=payload, timeout=5)

        # ❌ API failed
        if res.status_code != 200:
            print("API Error:", res.status_code, res.text)
            return "Not Verified"

        result = res.json()

        # ✅ Correct logic
        if "matches" in result:
            return "Threat Found"
        else:
            return "No Threat Found"

    except Exception as e:
        print("Safe browsing error:", e)
        return "Not Verified"