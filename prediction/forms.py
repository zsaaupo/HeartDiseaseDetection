from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import PredictionRecord


class HeartDiseasePredictionForm(forms.Form):
    """
    The ONLY fields on this form are the 10 features that were used to
    train the model in the notebook (in human-friendly form/order). No
    other dataset columns are exposed.

    Internal feature order required by the model is reconstructed in the
    view when calling predict_patient() -- it does not need to match the
    order of fields on this form.
    """

    age = forms.IntegerField(
        label="Age",
        min_value=1,
        max_value=120,
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 52",
        }),
    )

    sex = forms.TypedChoiceField(
        label="Sex",
        choices=PredictionRecord.SEX_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    chest_pain_type = forms.TypedChoiceField(
        label="Chest Pain Type",
        choices=PredictionRecord.CHEST_PAIN_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    resting_ecg = forms.TypedChoiceField(
        label="Resting ECG Result",
        choices=PredictionRecord.RESTING_ECG_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    max_heart_rate = forms.IntegerField(
        label="Maximum Heart Rate Achieved",
        min_value=60,
        max_value=220,
        validators=[MinValueValidator(60), MaxValueValidator(220)],
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 168",
        }),
    )

    exercise_induced_angina = forms.TypedChoiceField(
        label="Exercise Induced Angina",
        choices=PredictionRecord.EXANG_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    st_depression = forms.FloatField(
        label="ST Depression (Oldpeak)",
        min_value=0.0,
        max_value=10.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 1.0",
            "step": "0.1",
        }),
    )

    st_slope = forms.TypedChoiceField(
        label="ST Slope",
        choices=PredictionRecord.SLOPE_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    major_vessels = forms.TypedChoiceField(
        label="Number of Major Vessels",
        choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")],
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    thalassemia = forms.TypedChoiceField(
        label="Thalassemia",
        choices=PredictionRecord.THAL_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
