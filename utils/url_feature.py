import re
import tldextract

def extract_features(url):
    
    features = {}

    # URL Length
    features["URL_Length"] = len(url)

    # Check if URL has IP address
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    features["Has_IP"] = 1 if re.search(ip_pattern, url) else 0

    # Number of dots in URL
    features["Num_Dots"] = url.count(".")

    # HTTPS check
    features["HTTPS"] = 1 if url.startswith("https") else 0

    return features


# Test the function
'''if __name__ == "__main__":
    test_url = "https://google.com"
    result = extract_features(test_url)
    print(result)'''