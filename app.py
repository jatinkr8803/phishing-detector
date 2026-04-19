from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import os

from flask_cors import CORS

from utils.url_feature import extract_features
from utils.domain_age import get_domain_age
from utils.safe_browsing import check_safe_browsing

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL
# =========================
try:
    model = pickle.load(open("model/phishing_model.pkl", "rb"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model load error:", e)
    model = None


@app.route('/')
def home():
    return render_template('index.html')


# =========================
# PREDICT ROUTE
# =========================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"})

        print("\n🔍 URL:", url)

        # =========================
        # FEATURE EXTRACTION
        # =========================
        features = extract_features(url)
        features_df = pd.DataFrame([features])

        if model is not None:
            try:
                features_df = features_df.reindex(
                    columns=model.feature_names_in_,
                    fill_value=0
                )
            except:
                pass

        # =========================
        # ML PREDICTION (OPTIONAL)
        # =========================
        prediction = 0
        ai_score = 50

        if model is not None:
            try:
                prediction = int(model.predict(features_df)[0])

                try:
                    prob = model.predict_proba(features_df)[0][1]
                    ai_score = round(prob * 100, 2)
                except:
                    pass

            except Exception as e:
                print("ML error:", e)

        # =========================
        # DOMAIN AGE
        # =========================
        try:
            age = get_domain_age(url)
            domain_age = f"{age} days" if age != -1 else "Not Available"
        except:
            age = -1
            domain_age = "Not Available"

        # =========================
        # SAFE BROWSING
        # =========================
        try:
            safe = check_safe_browsing(url)
            safe_status = "Threat Found" if safe == "Threat Found" else "No Threat Found"
        except Exception as e:
            print("Safe browsing error:", e)
            safe_status = "No Threat Found"

        # =========================
        # 🔥 FINAL DECISION (YOUR LOGIC)
        # =========================
        SUSPICIOUS_THRESHOLD = 90  # days

        if safe_status == "Threat Found":
            final_prediction = 1   # phishing

        elif age != -1 and age < SUSPICIOUS_THRESHOLD:
            final_prediction = 2   # suspicious

        else:
            final_prediction = 0   # safe

        return jsonify({
            "prediction": int(final_prediction),
            "domain_age": domain_age,
            "safe_browsing": safe_status,
            "ai_score": ai_score
        })

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": "Server error"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)