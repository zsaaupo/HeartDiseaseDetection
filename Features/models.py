from django.db import models

class HeartDiseaseFeature(models.Model):
    age = models.IntegerField(help_text="Age of the patient")
    sex = models.IntegerField(choices=[(0, 'Female'), (1, 'Male')], help_text="Sex of the patient")
    chest_pain_type = models.IntegerField(help_text="Chest pain type (0-3)")
    resting_ecg = models.IntegerField(help_text="Resting electrocardiographic results (0-2)")
    max_heart_rate = models.IntegerField(help_text="Maximum heart rate achieved")
    exercise_induced_angina = models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], help_text="Exercise induced angina")
    st_depression = models.FloatField(help_text="ST depression induced by exercise relative to rest")
    st_slope = models.IntegerField(help_text="The slope of the peak exercise ST segment")
    major_vessels = models.IntegerField(help_text="Number of major vessels (0-3) colored by flourosopy")
    thalassemia = models.IntegerField(help_text="Thalassemia (1 = normal; 2 = fixed defect; 3 = reversable defect)")
    target = models.IntegerField(choices=[(0, 'No Disease'), (1, 'Disease')], null=True, blank=True, help_text="Prediction result")

    def __str__(self):
        return f"Patient {self.id} - Age: {self.age}, Target: {self.target}"
