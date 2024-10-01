from django.shortcuts import render
from .forms import MealPlannerForm
import requests

# Your Spoonacular API key
API_KEY = '789f7c2f742647cd8f9ac19833bd9323'

# BMR calculation function using the Harris-Benedict formula
def calculate_bmr(gender, weight, height_cm, age, activity_level):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height_cm) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height_cm) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'super active': 1.9
    }
    
    if activity_level not in activity_multipliers:
        raise ValueError("Invalid activity level")
    
    return bmr * activity_multipliers[activity_level]

# Function to calculate BMI
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # Convert height to meters
    return weight / (height_m ** 2)

# Function to recommend diet based on BMI and diabetes status
def get_diet_type(bmi, is_diabetic):
    if is_diabetic:
        if bmi >= 30:
            return 'low-carb'
        elif bmi >= 25:
            return 'low-fat'
        else:
            return 'balanced'
    else:
        if bmi >= 30:
            return 'low-carb'
        elif bmi >= 25:
            return 'low-fat'
        else:
            return 'balanced'

# Function to fetch meal plans for specific meal types
def get_meal_by_type(target_calories, diet_type, exclude_ingredients, meal_type):
    url = f"https://api.spoonacular.com/mealplanner/generate"
    params = {
        'apiKey': API_KEY,
        'timeFrame': 'day',
        'targetCalories': target_calories,
        'diet': diet_type,
        'excludeIngredients': exclude_ingredients
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        meals = data.get('meals', [])
        
        meal_count = 0
        meal_plan = []
        
        for meal in meals:
            if meal_count >= 3:  # Ensure at least 3 meals
                break
            meal_plan.append(meal)
            meal_count += 1
        
        return meal_plan
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

# Function to convert height from feet and inches to centimeters
def convert_height_to_cm(feet, inches):
    total_inches = (feet * 12) + inches
    return total_inches * 2.54  # Convert inches to centimeters

def meal_planner(request):
    if request.method == 'POST':
        form = MealPlannerForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            weight = form.cleaned_data['weight']
            height_feet = form.cleaned_data['height_feet']
            height_inches = form.cleaned_data['height_inches']
            age = form.cleaned_data['age']
            activity_level = form.cleaned_data['activity_level']
            is_diabetic = form.cleaned_data['is_diabetic']
            exclude_ingredients = "Pork,Bacon"

            # Convert height to centimeters
            height_cm = convert_height_to_cm(height_feet, height_inches)
            
            # Calculate BMR
            bmr = calculate_bmr(gender, weight, height_cm, age, activity_level)
            
            # Calculate BMI
            bmi = calculate_bmi(weight, height_cm)
            
            # Determine diet type
            diet_type = get_diet_type(bmi, is_diabetic)
            
            # Fetch meal plans
            breakfast_plan = get_meal_by_type(int(bmr), diet_type, exclude_ingredients, 'breakfast')
            lunch_plan = get_meal_by_type(int(bmr), diet_type, exclude_ingredients, 'lunch')
            dinner_plan = get_meal_by_type(int(bmr), diet_type, exclude_ingredients, 'dinner')

            bmr = format(bmr, '.2f')
            bmi = format(bmi, '.2f')
            
            # Render the result page
            return render(request, 'mlresult.html', {
                'bmr': bmr,
                'bmi': bmi,
                'diet_type': diet_type,
                'breakfast_plan': breakfast_plan,
                'lunch_plan': lunch_plan,
                'dinner_plan': dinner_plan
            })
    else:
        form = MealPlannerForm()
    
    return render(request, 'mlform.html', {'form': form})