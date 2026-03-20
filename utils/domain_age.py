# utils/domain_age.py

import whois
from datetime import datetime
import tldextract

def get_domain_age(url):
    try:
        ext = tldextract.extract(url)
        domain = ext.domain + "." + ext.suffix

        try:
            w = whois.whois(domain)
            creation_date = w.creation_date

            # If list → take first
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if not creation_date:
                return -1

            # 🔥 FIX: remove timezone
            if hasattr(creation_date, 'tzinfo') and creation_date.tzinfo is not None:
                creation_date = creation_date.replace(tzinfo=None)

            # Convert string → datetime
            if isinstance(creation_date, str):
                try:
                    creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
                except:
                    return -1

            # Now safe subtraction
            age_days = (datetime.now() - creation_date).days

            if 0 < age_days < 20000:
                return age_days

            return -1

        except Exception as e:
            print("WHOIS failed:", e)
            return -1

    except Exception as e:
        print("Domain error:", e)
        return -1