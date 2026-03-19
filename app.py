from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import traceback
import os

from utils.url_feature import extract_features
from utils.domain_age import get_domain_age
from utils.safe_browsing import check_safe_browsing

app = Flask(__name__)

# Load model
try:
    model = pickle.load(open("model/phishing_model.pkl", "rb"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model error:", e)
    model = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # -------------------------------
        # Feature extraction
        # -------------------------------
        features = extract_features(url)

        # -------------------------------
        # Domain age (FIXED)
        # -------------------------------
        try:
            domain_age = get_domain_age(url)  # returns -1 if fail
        except:
            domain_age = -1

        features["Domain_Age"] = 0 if domain_age == -1 else domain_age

        # -------------------------------
        # Safe browsing
        # -------------------------------
        try:
            safe_status = check_safe_browsing(url)  # True/False
        except:
            safe_status = True

        # -------------------------------
        # Model prediction
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
        # 🔥 FINAL DECISION LOGIC
        # -------------------------------
        score = 0

        if not safe_status:
            score += 2

        if prediction == 1:
            score += 2

        if domain_age != -1 and domain_age < 30:
            score += 1

        if score >= 3:
            final_result = "Phishing"
        elif score == 2:
            final_result = "Suspicious"
        else:
            final_result = "Legitimate"

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
        print("🔥 SERVER ERROR:")
        traceback.print_exc()

        return jsonify({
            "error": "Server crashed",
            "details": str(e)
        }), 500


# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))