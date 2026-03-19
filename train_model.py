import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("dataset/phishing_dataset.csv")

# Check column names
print(data.columns)

# Features and labels
X = data.drop("Result", axis=1)   # change if your label column is different
y = data["Result"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save trained model
with open("model/phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")