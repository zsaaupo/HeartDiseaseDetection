# CardioPredict — Heart Disease Prediction (Django 5)

A production-quality Django 5 application that wraps a scikit-learn
Logistic Regression model (reproduced exactly from
`Heart_Disease_Prediction.ipynb`) in a no-login dashboard, prediction form,
result page, and full prediction history.

---

## 1. Quick Start

### Live

Open the deployed app here:

[**LIVE**](https://heartdiseasedetection-2irk.onrender.com/)

No login is required. The app opens directly on the Dashboard.

### Local Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Run the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** — you land directly on the Dashboard. No
login is required anywhere in the app.

> The repository already have a trained `ml/heart_model.joblib` and
> `ml/heart_scaler.joblib`.

---

## 2. Application Flow

```
Dashboard  ──(Predict Heart Disease)──▶  Prediction Form
   ▲                                          │
   │                                   (submit & validate)
   │                                          ▼
   └──────(Go to Dashboard)───  Result Page  ──(Predict Again)──▶ Prediction Form
```

- **Dashboard** (`/`): statistic cards (Total / Positive / Negative
  predictions), three charts (outcome breakdown, risk-level breakdown,
  predictions-over-time), and a recent prediction history table with
  **View** and **Delete** actions.
- **Prediction Form** (`/predict/`): contains *only* the 10 features the
  model was trained on. Server-side validation (Django forms) plus a
  lightweight client-side check before submit.
- **Result Page** (`/predict/result/<id>/`): shows prediction, probability,
  risk level, and recommendation. Exactly two actions: **Predict Again**
  and **Go to Dashboard** — no other navigation appears on this page.
- **History Detail** (`/predict/history/<id>/`): full read-only detail of a
  past prediction, reachable from the dashboard table.

---

## 3. Machine Learning Pipeline

### 3.1 Executive Summary
This project aims to predict the presence of heart disease in patients using a clinical dataset. A Logistic Regression model was developed, achieving an accuracy of approximately **82.4%** and a ROC AUC score of **0.88**.

### 3.2 Data Overview & Preprocessing
- **Dataset**: The 'heart.csv' file contains 1,025 records with 14 original features.
- **Data Cleaning**: No missing values were detected. Features were renamed for better readability (e.g., `cp` to `Chest_Pain_Type`).
- **Feature Selection**: Based on importance, 10 key features were selected: `Thalassemia`, `Chest_Pain_Type`, `Major_Vessels`, `ST_Depression`, `Exercise_Induced_Angina`, `Max_Heart_Rate`, `ST_Slope`, `Age`, `Sex`, and `Resting_ECG`.
- **Scaling**: Data was standardized using `StandardScaler` to ensure all features contribute equally to the model.

### 3.3 Modeling: Logistic Regression
Logistic Regression was chosen as the primary classifier. It uses the sigmoid function to map linear combinations of inputs into probabilities.
- **Training Split**: 80% Train / 20% Test.
- **Hyperparameters**: `random_state=42` for reproducibility.

### 3.4 Performance Metrics
- **Accuracy**: 82.44%
- **ROC AUC**: 0.8841 (High diagnostic ability)
- **Precision/Recall**: 
    - **Recall for Class 1 (Disease)**: 0.90 (High sensitivity is crucial for medical diagnosis).
    - **Precision for Class 1**: 0.78.
- **Confusion Matrix**: Shows 76 True Negatives and 93 True Positives.

### 3.5 Key Insights from Visualizations
- **Coefficients**: `Chest_Pain_Type` and `ST_Slope` show significant positive correlations with heart disease, while `Major_Vessels` and `Sex` show strong negative correlations.
- **Feature Distribution**: Visual analysis confirms distinct distributions for features like `Max_Heart_Rate` and `ST_Depression` between healthy and diseased groups.
- **PR Curve**: The Precision-Recall AUC of 0.88 indicates robust performance even when balancing precision and recall.

### Risk level thresholds

Risk level is derived from the model's predicted probability of class `1`
(heart disease present):

| Probability | Risk Level |
|---|---|
| < 40% | Low |
| 40% – 70% | Medium |
| > 70% | High |

These thresholds live in `ml/predictor.py` (`LOW_RISK_MAX`,
`MEDIUM_RISK_MAX`) if you need to tune them.

---

## 4. Project Structure

```
HeartDiseasePrediction/
│
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
│
├── HeartDiseasePrediction/                 # Django project package
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
│
├── dashboard/                              # Dashboard app (stats, charts, history table)
│   ├── views.py
│   ├── urls.py
│
├── prediction/                             # Prediction form, result page, history CRUD
│   ├── models.py                           # PredictionRecord
│   ├── forms.py                            # HeartDiseasePredictionForm
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│
├── ml/                                     # Machine learning layer
│   ├── heart.csv                           # Training dataset
│   ├── Heart_Disease_Prediction.ipynb      # The notebook pipeline
│   ├── predictor.py                        # predict_patient() — the ONLY ML entry point
│   ├── heart_model.joblib                  # Trained LogisticRegression
│   └── heart_scaler.joblib                 # Fitted StandardScaler
│
├── templates/
│   ├── base.html                           # Full nav (Dashboard / New Prediction)
│   ├── base_minimal.html                   # Brand-only shell, used by the Result page
│   ├── dashboard/dashboard.html
│   └── prediction/
│       ├── form.html
│       ├── result.html
│       └── history_detail.html
│
├── static/
│   ├── css/style.css
│   └── js/main.js
│
└── media/                                  # Reserved for future use (e.g. PDF export)
```

---

## 5. Database

Every prediction is stored in SQLite (`prediction.PredictionRecord`):
date/time, all 10 input features, prediction (0/1), probability, and risk
level. The Dashboard's stats, charts, and history table all read live from
this table — nothing is cached or hard-coded.

To inspect the data via Django admin:

```bash
python manage.py createsuperuser
python manage.py runserver
# then visit /admin/
```

(Admin is read-only for prediction records by design — records should only
be created through the prediction workflow.)

---

## 6. Tech Stack

- Python 3.12+, Django 5
- scikit-learn + joblib for the ML layer
- SQLite (default Django database)
- Bootstrap 5 + Bootstrap Icons (via CDN)
- Chart.js (via CDN) for dashboard charts
- Vanilla JS for light client-side form checks and UX polish

---

## 7. Notes on the Form Fields

Only the 10 features used to train the model are exposed on the
Prediction Form (no other `heart.csv` columns, like resting blood pressure
or cholesterol, are collected or used):

| Field | Type | Notes |
|---|---|---|
| Age | number | 1–120 |
| Sex | select | Female / Male |
| Chest Pain Type | select | Typical Angina / Atypical Angina / Non-anginal Pain / Asymptomatic |
| Resting ECG Result | select | Normal / ST-T Wave Abnormality / Left Ventricular Hypertrophy |
| Max Heart Rate Achieved | number | 60–220 |
| Exercise Induced Angina | select | Yes / No |
| ST Depression (Oldpeak) | decimal | 0.0–10.0 |
| ST Slope | select | Upsloping / Flat / Downsloping |
| Number of Major Vessels | select | 0–4 |
| Thalassemia | select | Unknown / Fixed Defect / Normal / Reversible Defect |

---

## 8. Disclaimer

This application is a technical demonstration of an ML-powered Django
workflow. It is **not yet** a certified medical device and must not be used
for real clinical decision-making.
