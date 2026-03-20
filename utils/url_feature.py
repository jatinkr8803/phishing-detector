import re
import tldextract

def extract_features(url):
    features = {}

    url_lower = url.lower()

    # -------------------------------
    # BASIC FEATURES
    # -------------------------------
    features["URL_Length"] = len(url)
    features["Num_Dots"] = url.count(".")
    features["HTTPS"] = 1 if url.startswith("https") else 0

    # -------------------------------
    # IP ADDRESS
    # -------------------------------
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    features["Has_IP"] = 1 if re.search(ip_pattern, url) else 0

    # -------------------------------
    # SPECIAL CHARACTERS
    # -------------------------------
    features["Num_Hyphens"] = url.count("-")
    features["Num_At"] = url.count("@")
    features["Num_Question"] = url.count("?")
    features["Num_Equal"] = url.count("=")

    # -------------------------------
    # SUSPICIOUS KEYWORDS
    # -------------------------------
    suspicious_words = [
        "login", "verify", "secure", "account",
        "update", "bank", "paypal", "signin",
        "confirm", "password"
    ]

    features["Has_Suspicious_Words"] = 1 if any(word in url_lower for word in suspicious_words) else 0

    # -------------------------------
    # DOMAIN INFO
    # -------------------------------
    ext = tldextract.extract(url)
    domain = ext.domain

    features["Domain_Length"] = len(domain)

    # -------------------------------
    # BRAND MISUSE
    # -------------------------------
    brands = ["google", "facebook", "paypal", "amazon", "bank"]

    features["Has_Brand"] = 1 if any(b in url_lower for b in brands) else 0

    return features