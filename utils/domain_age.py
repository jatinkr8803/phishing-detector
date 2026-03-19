import whois
from datetime import datetime
import tldextract

def get_domain_age(url):
    try:
        ext = tldextract.extract(url)
        domain = ext.domain + "." + ext.suffix

        w = whois.whois(domain)

        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            age_days = (datetime.now(creation_date.tzinfo) - creation_date).days
            return age_days
        else:
            return 0

    except Exception as e:
        print("WHOIS error:", e)
        return -1


'''if __name__ == "__main__":
    urls = ["google.com", "facebook.com", "amazon.com"]

    for url in urls:
        print(url, "->", get_domain_age(url))'''