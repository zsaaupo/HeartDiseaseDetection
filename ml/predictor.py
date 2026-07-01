"""
predictor.py
------------
Single source of truth for running inference with the trained heart-disease
Logistic Regression model.

The model and scaler are loaded ONCE at import time (Django imports this
module a single time per worker process, at server start), and the rest of
the application must ONLY interact with the model through the
`predict_patient()` function defined here.

Usage:
    from ml.predictor import predict_patient

    result = predict_patient({
        "Age": 52, "Sex": 1, "Chest_Pain_Type": 0, "Resting_ECG": 1,
        "Max_Heart_Rate": 168, "Exercise_Induced_Angina": 0,
        "ST_Depression": 1.0, "ST_Slope": 2, "Major_Vessels": 2,
        "Thalassemia": 3,
    })
    # result -> {
    #     "prediction": 0,
    #     "prediction_label": "No Heart Disease Detected",
    #     "probability": 0.0734,            # probability of class 1 (disease)
    #     "probability_percent": "7.34%",
    #     "risk_level": "Low",
    #     "recommendation": "...",
    # }
"""

import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "heart_model.joblib")
SCALER_PATH = os.path.join(BASE_DIR, "heart_scaler.joblib")

# Exact feature order the model/scaler were fit with. MUST match
# ml/train_model.py FEATURE_ORDER exactly, in both names and order.
FEATURE_ORDER = [
    "Thalassemia",
    "Chest_Pain_Type",
    "Major_Vessels",
    "ST_Depression",
    "Exercise_Induced_Angina",
    "Max_Heart_Rate",
    "ST_Slope",
    "Age",
    "Sex",
    "Resting_ECG",
]

# Risk-level thresholds applied to the predicted probability of class 1
# (heart disease present).
LOW_RISK_MAX = 0.40
MEDIUM_RISK_MAX = 0.70

RECOMMENDATIONS = {
    "Low": (
        "Your results suggest a low likelihood of heart disease. "
        "Continue maintaining a heart-healthy lifestyle and attend routine check-ups."
    ),
    "Medium": (
        "Your results suggest a moderate likelihood of heart disease. "
        "Please consider scheduling an appointment with a physician for further evaluation."
    ),
    "High": (
        "Your results suggest a high likelihood of heart disease. "
        "Please consult a cardiologist for further medical evaluation as soon as possible."
    ),
}

_model = None
_scaler = None


def _load_artifacts():
    """Load the joblib model and scaler into module-level globals (once)."""
    global _model, _scaler
    if _model is None or _scaler is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(
                "Trained model/scaler not found. Run `python ml/train_model.py` "
                "from the project root before starting the server."
            )
        _model = joblib.load(MODEL_PATH)
        _scaler = joblib.load(SCALER_PATH)
    return _model, _scaler


# Load immediately at import time, so Django only pays this cost once,
# when the module is first imported (server startup / first request).
_load_artifacts()


def _determine_risk_level(probability: float) -> str:
    if probability < LOW_RISK_MAX:
        return "Low"
    elif probability < MEDIUM_RISK_MAX:
        return "Medium"
    return "High"


def predict_patient(data: dict) -> dict:
    """
    Run a prediction for a single patient.

    Parameters
    ----------
    data : dict
        Must contain all of FEATURE_ORDER as keys.

    Returns
    -------
    dict with keys:
        prediction (int 0/1), prediction_label (str), probability (float 0-1),
        probability_percent (str), risk_level (str), recommendation (str)
    """
    model, scaler = _load_artifacts()

    missing = [f for f in FEATURE_ORDER if f not in data]
    if missing:
        raise ValueError(f"Missing required feature(s): {missing}")

    # Build the row in the EXACT order the scaler/model expect, as a
    # DataFrame with matching column names (avoids sklearn's "missing
    # feature names" warning and guards against silent column misordering).
    row = pd.DataFrame(
        [[float(data[feature]) for feature in FEATURE_ORDER]],
        columns=FEATURE_ORDER,
    )

    scaled = scaler.transform(row)

    prediction = int(model.predict(scaled)[0])
    probability = float(model.predict_proba(scaled)[0][1])  # P(class == 1)

    risk_level = _determine_risk_level(probability)

    return {
        "prediction": prediction,
        "prediction_label": "Heart Disease Detected" if prediction == 1 else "No Heart Disease Detected",
        "probability": probability,
        "probability_percent": f"{probability * 100:.2f}%",
        "risk_level": risk_level,
        "recommendation": RECOMMENDATIONS[risk_level],
    }
