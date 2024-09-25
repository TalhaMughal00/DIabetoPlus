from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Predictions Model
class Predictions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    age = models.IntegerField()
    hypertension = models.BooleanField()
    heart_disease = models.BooleanField()
    smoking_history = models.CharField(max_length=50)
    bmi = models.FloatField()
    hba1c_level = models.FloatField()
    blood_glucose_level = models.FloatField()
    prediction_result = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User ID: {self.user.id} - {self.date}"
    