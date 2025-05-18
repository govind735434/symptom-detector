import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
df = pd.read_csv("data/Disease precaution.csv")

# Check required columns
required_cols = ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

# Combine precaution columns
df['Precautions'] = df[required_cols].fillna('').agg(' '.join, axis=1).str.strip()
df['Precautions'] = df['Precautions'].str.replace(r'[^a-zA-Z ]', ' ', regex=True)
df['Precautions'] = df['Precautions'].str.lower().str.strip()
df['Precautions'] = df['Precautions'].replace(r'\s+', ' ', regex=True)
df = df[df['Precautions'] != '']

print("Disease counts:", df['Disease'].value_counts())

X = df['Precautions']
y = df['Disease']

le = LabelEncoder()
y_encoded = le.fit_transform(y)

vectorizer = TfidfVectorizer(stop_words=None)
X_vectorized = vectorizer.fit_transform(X)

# Train on full dataset (no train/test split, since each class has 1 sample)
model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
model.fit(X_vectorized, y_encoded)

# Save everything
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/disease_precaution_xgb_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(le, "models/label_encoder.pkl")

print("Model trained on full dataset. No test split due to single samples per class.")