from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import traceback
import os

from utils.url_feature import extract_features
from utils.domain_age import get_domain_age
from utils.safe_browsing import check_safe_browsing

app = Flask(__name__)

# -------------------------------
# LOAD MODEL
# -------------------------------
try:
    model = pickle.load(open("model/phishing_model.pkl", "rb"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model error:", e)
    model = None


# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# ANALYZE
# -------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # -------------------------------
        # FEATURES
        # -------------------------------
        features = extract_features(url)

        # -------------------------------
        # DOMAIN AGE
        # -------------------------------
        try:
            domain_age = get_domain_age(url)
        except:
            domain_age = -1

        features["Domain_Age"] = 0 if domain_age == -1 else domain_age

        # -------------------------------
        # SAFE BROWSING
        # -------------------------------
        try:
            safe_status = check_safe_browsing(url)
        except:
            safe_status = True

        # -------------------------------
        # MODEL
        # -------------------------------
        df = pd.DataFrame([features])

        if model is not None:
            try:
                df = df.reindex(columns=model.feature_names_in_, fill_value=0)
                prediction = model.predict(df)[0]
            except:
                prediction = 0
        else:
            prediction = 0

        # -------------------------------
        # FLAGS
        # -------------------------------
        url_lower = url.lower()

        suspicious_keywords = ["login", "verify", "secure", "account", "bank"]
        keyword_flag = any(word in url_lower for word in suspicious_keywords)

        new_domain_flag = (domain_age != -1 and domain_age < 30)
        ml_flag = (prediction == 1)
        blacklist_flag = (not safe_status)

        # -------------------------------
        # FINAL DECISION (FIXED)
        # -------------------------------
        if blacklist_flag:
            final_result = "Phishing"

        elif ml_flag:
            final_result = "Phishing"

        elif keyword_flag and new_domain_flag:
            final_result = "Phishing"

        elif new_domain_flag:
            final_result = "Suspicious"

        else:
            final_result = "Legitimate"

        # -------------------------------
        # DEBUG (IMPORTANT)
        # -------------------------------
        print({
            "url": url,
            "prediction_raw": prediction,
            "safe_status": safe_status,
            "domain_age": domain_age,
            "ml_flag": ml_flag,
            "keyword_flag": keyword_flag,
            "new_domain_flag": new_domain_flag
        })

        # -------------------------------
        # RESPONSE
        # -------------------------------
        return jsonify({
            "url": url,
            "prediction": final_result,
            "safe_browsing": "Safe" if safe_status else "Danger",
            "domain_age_days": domain_age
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# -------------------------------
# RUN (RENDER FIX)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)