from django.db import models


class PredictionRecord(models.Model):
    """Stores every prediction made through the app, including all of the
    raw input features, so the full history can be displayed/audited later.
    """

    SEX_CHOICES = [
        (0, "Female"),
        (1, "Male"),
    ]

    CHEST_PAIN_CHOICES = [
        (0, "Typical Angina"),
        (1, "Atypical Angina"),
        (2, "Non-anginal Pain"),
        (3, "Asymptomatic"),
    ]

    RESTING_ECG_CHOICES = [
        (0, "Normal"),
        (1, "ST-T Wave Abnormality"),
        (2, "Left Ventricular Hypertrophy"),
    ]

    EXANG_CHOICES = [
        (0, "No"),
        (1, "Yes"),
    ]

    SLOPE_CHOICES = [
        (0, "Upsloping"),
        (1, "Flat"),
        (2, "Downsloping"),
    ]

    THAL_CHOICES = [
        (0, "Unknown"),
        (1, "Fixed Defect"),
        (2, "Normal"),
        (3, "Reversible Defect"),
    ]

    RISK_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    # --- Input features (exact set used to train the model) ---
    age = models.PositiveSmallIntegerField(help_text="Age in years")
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES)
    chest_pain_type = models.PositiveSmallIntegerField(choices=CHEST_PAIN_CHOICES)
    resting_ecg = models.PositiveSmallIntegerField(choices=RESTING_ECG_CHOICES)
    max_heart_rate = models.PositiveSmallIntegerField(help_text="Maximum heart rate achieved")
    exercise_induced_angina = models.PositiveSmallIntegerField(choices=EXANG_CHOICES)
    st_depression = models.FloatField(help_text="ST depression induced by exercise relative to rest")
    st_slope = models.PositiveSmallIntegerField(choices=SLOPE_CHOICES)
    major_vessels = models.PositiveSmallIntegerField(help_text="Number of major vessels (0-4) colored by fluoroscopy")
    thalassemia = models.PositiveSmallIntegerField(choices=THAL_CHOICES)

    # --- Output ---
    prediction = models.PositiveSmallIntegerField(help_text="0 = No Heart Disease, 1 = Heart Disease")
    probability = models.FloatField(help_text="Predicted probability of heart disease (0-1)")
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Prediction Record"
        verbose_name_plural = "Prediction Records"

    def __str__(self):
        return f"Prediction #{self.pk} - {self.get_prediction_display_label()} ({self.created_at:%Y-%m-%d %H:%M})"

    def get_prediction_display_label(self):
        return "Heart Disease Detected" if self.prediction == 1 else "No Heart Disease Detected"

    @property
    def probability_percent(self):
        return f"{self.probability * 100:.2f}%"
