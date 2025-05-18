# 🩺 Symptom Detector

A web-based AI-powered application that helps users identify possible health conditions based on their input symptoms. The app uses a trained machine learning model and a static rule-based symptom matcher to provide fast and intelligent health-related insights.

## 🔍 Features

- Detect symptoms from user input text
- Predict diseases using a trained XGBoost model
- Show matching conditions from a static symptom-disease dictionary
- Responsive frontend with background imagery
- Lightweight and easy to deploy

## 🚀 How It Works

1. **Frontend**: Accepts user symptom descriptions via a textarea and shows possible conditions from:
   - A static dictionary
   - A machine learning prediction

2. **Backend (Flask)**:
   - Loads a trained model (`XGBoost`)
   - Processes the input using `TfidfVectorizer`
   - Outputs the most likely disease

3. **Training**:
   - Model trained on precaution data (`Disease precaution.csv`)
   - Uses `TF-IDF` + `LabelEncoder` + `XGBoostClassifier`

## 🗃️ Tech Stack

- Python
- Flask
- XGBoost
- Scikit-learn
- HTML/CSS/JavaScript

## 🛠️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/symptom-detector.git
   cd symptom-detector
