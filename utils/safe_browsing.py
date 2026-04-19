# utils/safe_browsing.py

import requests
import os

def check_safe_browsing(url):
    try:
        API_KEY = os.environ.get("API_KEY")

        # 🔒 If API key missing → fallback safe
        if not API_KEY:
            print("⚠️ Safe Browsing API key missing")
            return "No Threat Found"

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

        # ❌ API failure → fallback safe
        if res.status_code != 200:
            print("⚠️ Safe Browsing API error:", res.status_code)
            return "No Threat Found"

        result = res.json()

        # ✅ FINAL CHECK
        if "matches" in result:
            return "Threat Found"
        else:
            return "No Threat Found"

    except Exception as e:
        print("⚠️ Safe Browsing Exception:", e)
        return "No Threat Found"