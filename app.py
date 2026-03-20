# app.py

from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

from utils.url_feature import extract_features
from utils.domain_age import get_domain_age
from utils.safe_browsing import check_safe_browsing

app = Flask(__name__)

# Load model
try:
    model = pickle.load(open("model/phishing_model.pkl", "rb"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model load error:", e)
    model = None


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")

        print("\n🔍 URL:", url)

        # =========================
        # STEP 1: Feature Extraction
        # =========================
        features = extract_features(url)
        features_df = pd.DataFrame([features])

        # Align with model
        if model is not None:
            try:
                features_df = features_df.reindex(
                    columns=model.feature_names_in_,
                    fill_value=0
                )
            except:
                pass

        print("✅ Features extracted")

        # =========================
        # STEP 2: ML
        # =========================
        prediction = 0
        ai_score = 0

        if model is not None:
            try:
                prediction = model.predict(features_df)[0]

                try:
                    prob = model.predict_proba(features_df)[0][1]
                    ai_score = round(prob * 100, 2)
                except:
                    ai_score = 50

                print("✅ ML done")

            except Exception as e:
                print("❌ ML error:", e)

        # =========================
        # STEP 3: Domain Age
        # =========================
        try:
            age = get_domain_age(url)
            domain_age = f"{age} days" if age != -1 else "Not Available"
            print("✅ Domain age:", domain_age)
        except:
            domain_age = "Not Available"

        # =========================
        # STEP 4: Safe Browsing
        # =========================
        try:
            safe = check_safe_browsing(url)

            if safe is True:
                safe_status = "Safe ✅"
            elif safe is False:
                safe_status = "Dangerous ❌"
            else:
                safe_status = "Unknown ⚠️"

            print("✅ Safe browsing:", safe_status)

        except:
            safe_status = "Unknown ⚠️"
            safe = None

        # =========================
        # STEP 5: FINAL DECISION (SMART FIX)
        # =========================

        # Rule 1: Blacklisted → always phishing
        if safe is False:
            final_prediction = 1

        # Rule 2: Old domain → trust it (ignore ML false positives)
        elif age != -1 and age > 180:
            final_prediction = 0

        # Rule 3: New domain + ML suspicious → phishing
        elif prediction == 1 and age != -1 and age <= 180:
            final_prediction = 1

        # Rule 4: Otherwise safe
        else:
            final_prediction = 0
        print("✅ Response ready\n")

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
    app.run(debug=True)