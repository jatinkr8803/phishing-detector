import whois
from datetime import datetime
import tldextract
import time

def get_domain_age(url):
    try:
        ext = tldextract.extract(url)
        domain = ext.domain + "." + ext.suffix

        # 🔁 Retry (WHOIS unstable)
        for _ in range(2):
            try:
                w = whois.whois(domain)
                creation_date = w.creation_date

                # Handle list
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]

                # If string → convert
                if isinstance(creation_date, str):
                    try:
                        creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
                    except:
                        return -1

                # If valid date
                if creation_date:
                    age_days = (datetime.now() - creation_date).days

                    # 🔒 Avoid negative/invalid
                    if age_days < 0 or age_days > 20000:
                        return -1

                    return age_days

            except:
                time.sleep(1)

        return -1

    except Exception as e:
        print("WHOIS error:", e)
        return -1