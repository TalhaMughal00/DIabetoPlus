from django.db import models
from django.contrib.auth.models import User

# Exercise Model
class ER(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    exercises = models.JSONField()  # Store exercises as JSON
    intensity = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Routine"

# Diet Plan Model
class DP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breakfast_plan = models.JSONField()  # Storing the meal plan as JSON
    lunch_plan = models.JSONField()
    dinner_plan = models.JSONField()
    bmr = models.FloatField()
    bmi = models.FloatField()
    diet_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Meal Plan"
