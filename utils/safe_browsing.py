import requests
import os

API_KEY = os.environ.get("API_KEY")

def check_safe_browsing(url):
    try:
        if not API_KEY:
            return True  # assume safe if no key

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

        # 🔥 FIX: return BOOLEAN
        if "matches" in result:
            return False   # ❌ dangerous
        else:
            return True    # ✅ safe

    except:
        return True  # fail-safe