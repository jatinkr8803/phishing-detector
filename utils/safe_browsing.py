import requests
import os

def check_safe_browsing(url):
    try:
        API_KEY = os.environ.get("API_KEY")

        if not API_KEY:
            print("⚠️ API key missing")
            return "API key missing"

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

        if res.status_code != 200:
            print("⚠️ API error:", res.status_code)
            return "Unknown"

        result = res.json()

        if "matches" in result:
            return "Threat Found"
        else:
            return "No Threat Found"

    except Exception as e:
        print("⚠️ Exception:", e)
        return "Unknown"