from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import re
from flask_cors import CORS

from utils.domain_age import get_domain_age
from utils.safe_browsing import check_safe_browsing

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL ONLY
# =========================
model = pickle.load(open("model/phishing_model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')


# =========================
# FEATURE GENERATION
# =========================
def generate_features(url):
    return {
        'having_IP_Address': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        'URL_Length': 0 if len(url) < 54 else (1 if len(url) <= 75 else 2),
        'Shortining_Service': 1 if "bit.ly" in url else 0,
        'having_At_Symbol': 1 if "@" in url else 0,
        'double_slash_redirecting': 1 if url.count("//") > 1 else 0,
        'Prefix_Suffix': 1 if "-" in url else 0,
        'having_Sub_Domain': 1 if url.count('.') > 2 else 0,
        'SSLfinal_State': 1 if url.startswith("https") else 0,
        'HTTPS_token': 1 if "https" in url else 0
    }


@app.route('/predict', methods=['POST'])
def predict():
    try:
        url = request.json.get("url")

        if not url:
            return jsonify({"error": "No URL provided"})

        # Features
        features = generate_features(url)
        df = pd.DataFrame([features])
        df = df.reindex(columns=model.feature_names_in_, fill_value=0)

        # ML
        prediction = int(model.predict(df)[0])
        prob = model.predict_proba(df)[0][1] * 100

        # External checks
        age = get_domain_age(url)
        safe = check_safe_browsing(url)

        # Final logic
        if "@" in url or "bit.ly" in url:
            final = 1
        elif safe == "Threat Found":
            final = 1
        elif prediction == 1 and age != -1 and age < 90:
            final = 1
        elif prediction == 1:
            final = 2
        elif age != -1 and age < 90:
            final = 2
        else:
            final = 0

        return jsonify({
            "prediction": final,
            "ai_score": round(prob, 2),
            "domain_age": age if age != -1 else "Not Available",
            "safe_browsing": safe
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Server error"})


if __name__ == "__main__":
    app.run(debug=True)