from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MealPlannerForm
from .forms import BMICalculatorForm
import requests
import random
from .models import ER
from .models import DP
from django.contrib import messages

# Your Spoonacular API key
API_KEY = ''

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
def get_diet_type(bmi):
    if bmi >= 30:
        return 'low-carb'
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

@login_required
def meal_planner(request):
    form = MealPlannerForm()
    breakfast_plan = lunch_plan = dinner_plan = bmr = bmi = diet_type = None  # Initialize variables

    if request.method == 'POST':
        form = MealPlannerForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            weight = form.cleaned_data['weight']
            height_feet = form.cleaned_data['height_feet']
            height_inches = form.cleaned_data['height_inches']
            age = form.cleaned_data['age']
            activity_level = form.cleaned_data['activity_level']
            exclude_ingredients = "Pork,Bacon"

            # Convert height to centimeters
            height_cm = convert_height_to_cm(height_feet, height_inches)
            
            # Calculate BMR
            bmr = calculate_bmr(gender, weight, height_cm, age, activity_level)
            
            # Calculate BMI
            bmi = calculate_bmi(weight, height_cm)
            
            # Determine diet type
            diet_type = get_diet_type(bmi)
            
            # Fetch meal plans
            breakfast_plan = get_meal_by_type(int(bmr), diet_type, exclude_ingredients, 'breakfast')
            lunch_plan = get_meal_by_type(int(bmr), diet_type, exclude_ingredients, 'lunch')
            dinner_plan = get_meal_by_type(int(bmr), diet_type, exclude_ingredients, 'dinner')

            # Save diet plan to the database, updating if it already exists
            diet_plan, created = DP.objects.update_or_create(
                user=request.user,
                defaults={
                    'breakfast_plan': breakfast_plan,
                    'lunch_plan': lunch_plan,
                    'dinner_plan': dinner_plan,
                    'bmr': bmr,
                    'bmi': bmi,
                    'diet_type': diet_type
                }
            )

            # Format BMR and BMI for display
            bmr = format(bmr, '.2f')
            bmi = format(bmi, '.2f')

            # Success message based on whether a new plan was created or updated
            if created:
                messages.success(request, 'Diet Plan Created Successfully!')
            else:
                messages.success(request, 'Diet Plan Updated Successfully!')
    
    # Render the form and meal plan results in the same template
    return render(request, 'mlform.html', {
        'form': form,
        'bmr': bmr,
        'bmi': bmi,
        'diet_type': diet_type,
        'breakfast_plan': breakfast_plan,
        'lunch_plan': lunch_plan,
        'dinner_plan': dinner_plan
    })

# Exercise Routine 
def get_exercises(body_parts=None, equipment=None, limit=8, offset=0):
    url = "https://exercisedb.p.rapidapi.com/exercises"
    headers = {
        "X-RapidAPI-Host": "",
        "X-RapidAPI-Key": ""
    }
    params = {'limit': limit, 'offset': offset}
    
    if body_parts:
        params['bodyPart'] = body_parts
    if equipment:
        params['equipment'] = equipment

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        exercises = response.json()
        return exercises
    else:
        return None

def determine_intensity(bmi):
    if bmi < 18.5:
        return "Low"
    elif 18.5 <= bmi < 24.9:
        return "Moderate"
    elif 25 <= bmi < 29.9:
        return "High"
    else:
        return "Very High"

@login_required
def exercise_view(request):
    form = BMICalculatorForm()
    exercises = []
    intensity = None
    
    # Check if a routine exists for the user
    try:
        exercise_routine = ER.objects.get(user=request.user)
        exercises = exercise_routine.exercises
        intensity = exercise_routine.intensity
    except ER.DoesNotExist:
        exercise_routine = None
    
    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        
        if form.is_valid():
            # Get form data
            feet = form.cleaned_data['feet']
            inches = form.cleaned_data['inches']
            weight = form.cleaned_data['weight']

            # Convert height to cm and calculate BMI
            height_cm = convert_height_to_cm(feet, inches)
            bmi = calculate_bmi(weight, height_cm)
            intensity = determine_intensity(bmi)

            # Fetch exercises
            body_parts = ['chest', 'back', 'legs', 'arms', 'core']
            equipment_options = ['none', 'dumbbell', 'barbell', 'kettlebell', 'resistance band', 'medicine ball']

            fetched_exercises_count = 0
            total_exercises_to_fetch = 8
            exercises = []

            while fetched_exercises_count < total_exercises_to_fetch:
                body_part = random.choice(body_parts)
                equipment = random.choice(equipment_options)
                limit = total_exercises_to_fetch - fetched_exercises_count
                
                fetched_exercises = get_exercises(body_parts=body_part, equipment=equipment, limit=limit)

                if fetched_exercises:
                    exercises.extend(fetched_exercises)
                    fetched_exercises_count += len(fetched_exercises)

            # Save or update the exercise routine
            if exercise_routine:
                # Update existing routine
                exercise_routine.exercises = exercises
                exercise_routine.intensity = intensity
                exercise_routine.save()
                messages.success(request, 'Exercise Routine Updated Successfully!')
            else:
                # Create new routine
                ER.objects.create(
                    user=request.user,
                    exercises=exercises,
                    intensity=intensity
                )
                messages.success(request, 'Exercise Routine Created Successfully!')
    return render(request, 'exercise.html', {'form': form, 'exercises': exercises, 'intensity': intensity})




