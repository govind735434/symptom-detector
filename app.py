from flask import Flask, request, jsonify, render_template
import joblib
import os

# Load the model and preprocessors
model = joblib.load("models/disease_precaution_xgb_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Make sure index.html is in the 'templates' folder

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        user_input = data.get("text", "")
        
        if not user_input.strip():
            return jsonify({"error": "Empty input"}), 400

        # Preprocess the input
        cleaned = user_input.lower()
        cleaned = ''.join([c if c.isalpha() or c.isspace() else ' ' for c in cleaned])
        cleaned = ' '.join(cleaned.split())

        # Vectorize input
        X_input = vectorizer.transform([cleaned])
        y_pred = model.predict(X_input)
        predicted_label = label_encoder.inverse_transform(y_pred)[0]

        return jsonify({"predicted_disease": predicted_label})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
