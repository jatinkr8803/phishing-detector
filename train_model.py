import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv("dataset/phishing_dataset.csv")

print("📊 Columns:", data.columns.tolist())

# AUTO COLUMN DETECTION
def find_column(keyword):
    for col in data.columns:
        if keyword.lower() in col.lower():
            return col
    return None

col_map = {
    'having_IP_Address': find_column("IP"),
    'URL_Length': find_column("URL_Length"),
    'Shortining_Service': find_column("Shortining_Service"),
    'having_At_Symbol': find_column("At_Symbol"),
    'double_slash_redirecting': find_column("double_slash"),
    'Prefix_Suffix': find_column("Prefix_Suffix"),
    'having_Sub_Domain': find_column("Sub_Domain"),
    'SSLfinal_State': find_column("SSL"),
    'HTTPS_token': find_column("HTTPS_token")
}

print("\n🔍 Mapping:")
for k,v in col_map.items():
    print(k, "→", v)

# BUILD DATA
X = pd.DataFrame()
for new, old in col_map.items():
    X[new] = data[old]

y = data["Result"]

X = X.fillna(0)

# TRAIN
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

# EVAL
pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, pred))

# SAVE
pickle.dump(model, open("model/phishing_model.pkl", "wb"))

print("🔥 DONE")