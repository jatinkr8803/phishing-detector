import re
import tldextract

def extract_features(url):

    features = {}

    # BASIC
    features['having_IP_Address'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    features['URL_Length'] = len(url)
    features['Shortining_Service'] = 1 if "bit.ly" in url else 0
    features['having_At_Symbol'] = 1 if "@" in url else 0
    features['double_slash_redirecting'] = 1 if "//" in url[8:] else 0
    features['Prefix_Suffix'] = 1 if "-" in url else 0

    # DOMAIN
    ext = tldextract.extract(url)
    domain = ext.domain

    features['having_Sub_Domain'] = 1 if url.count('.') > 2 else 0
    features['Domain_registeration_length'] = 1
    features['Favicon'] = 1

    # HTTPS
    features['SSLfinal_State'] = 1 if url.startswith("https") else 0
    features['HTTPS_token'] = 1 if "https" in domain else 0

    # REQUESTS
    features['Request_URL'] = 0
    features['URL_of_Anchor'] = 0
    features['Links_in_tags'] = 0

    # SCRIPT
    features['SFH'] = 0
    features['Submitting_to_email'] = 0
    features['Redirect'] = 0
    features['on_mouseover'] = 0
    features['RightClick'] = 0
    features['popUpWidnow'] = 0
    features['Iframe'] = 0

    # DOMAIN AGE / TRAFFIC
    features['age_of_domain'] = 1
    features['DNSRecord'] = 1
    features['web_traffic'] = 1
    features['Page_Rank'] = 1
    features['Google_Index'] = 1
    features['Links_pointing_to_page'] = 1
    features['Statistical_report'] = 0

    return features