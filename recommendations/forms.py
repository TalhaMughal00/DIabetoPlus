from django import forms

class MealPlannerForm(forms.Form):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('lightly active', 'Lightly Active'),
        ('moderately active', 'Moderately Active'),
        ('very active', 'Very Active'),
        ('super active', 'Super Active')
    ]
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    weight = forms.FloatField(label="Weight (in kg)")
    height_feet = forms.IntegerField(label="Height (feet)")
    height_inches = forms.IntegerField(label="Height (inches)")
    age = forms.IntegerField(label="Age")
    activity_level = forms.ChoiceField(choices=ACTIVITY_CHOICES)
    
class BMICalculatorForm(forms.Form):
    feet = forms.IntegerField(label="Height (feet)", min_value=0)
    inches = forms.IntegerField(label="Height (inches)", min_value=0, max_value=11)
    weight = forms.FloatField(label="Weight (kg)", min_value=0.0)
