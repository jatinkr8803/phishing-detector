# -------------------------------
# 🔥 STRONG SECURITY LOGIC (FINAL)
# -------------------------------

# Rule 1: Suspicious keywords
suspicious_keywords = [
    "login", "verify", "update", "secure",
    "account", "bank", "paypal", "facebook"
]

url_lower = url.lower()

keyword_flag = any(word in url_lower for word in suspicious_keywords)

# Rule 2: New domain
new_domain_flag = (domain_age != -1 and domain_age < 30)

# Rule 3: ML model
ml_flag = (prediction == 1)

# Rule 4: Safe browsing
blacklist_flag = (not safe_status)

# -------------------------------
# FINAL DECISION
# -------------------------------
if blacklist_flag:
    final_result = "Phishing"

elif keyword_flag and new_domain_flag:
    final_result = "Phishing"

elif ml_flag:
    final_result = "Phishing"

elif new_domain_flag:
    final_result = "Suspicious"

else:
    final_result = "Legitimate"