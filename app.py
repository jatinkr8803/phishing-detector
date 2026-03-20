from flask import Flask, request, jsonify, render_template, send_from_directory
import pickle
import pandas as pd
import os

from flask_cors import CORS

from utils.url_feature import extract_features
from utils.domain_age import get_domain_age
from utils.safe_browsing import check_safe_browsing

app = Flask(__name__)
CORS(app)

# ✅ Load model safely
try:
    model = pickle.load(open("model/phishing_model.pkl", "rb"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model load error:", e)
    model = None


# ✅ FIXED: Render frontend UI
@app.route('/')
def home():
    return render_template('index.html')


# ✅ Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"})

        print("\n🔍 URL:", url)

        # STEP 1: Feature Extraction
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

        # STEP 2: ML Prediction
        prediction = 0
        ai_score = 0

        if model is not None:
            try:
                prediction = int(model.predict(features_df)[0])

                try:
                    prob = model.predict_proba(features_df)[0][1]
                    ai_score = round(prob * 100, 2)
                except:
                    ai_score = 50
            except Exception as e:
                print("❌ ML error:", e)

        # STEP 3: Domain Age
        try:
            age = get_domain_age(url)
            domain_age = f"{age} days" if age != -1 else "Not Available"
        except:
            age = -1
            domain_age = "Not Available"

        # STEP 4: Safe Browsing
        try:
            safe = check_safe_browsing(url)

            if safe == "Threat Found":
                safe_status = "Threat Found"
            elif safe == "No Threat Found":
                safe_status = "No Threat Found"
            else:
                safe_status = "Not Verified"

        except Exception as e:
            print("Safe Browsing Error:", e)
            safe = None
            safe_status = "Not Verified"

        # STEP 5: FINAL DECISION LOGIC
        if safe == "Threat Found":
            final_prediction = 1
        elif age != -1 and age > 180:
            final_prediction = 0
        elif prediction == 1 and age != -1 and age <= 180:
            final_prediction = 1
        else:
            final_prediction = 0

        return jsonify({
            "prediction": int(final_prediction),
            "domain_age": domain_age,
            "safe_browsing": safe_status,
            "ai_score": ai_score
        })

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": "Server error"})


# ✅ Google verification
@app.route('/google1234567890abcdef.html')
def google_verification():
    return send_from_directory('static', 'google1234567890abcdef.html')


# ✅ Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)