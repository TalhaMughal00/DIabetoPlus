from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import joblib
import pandas as pd
from django.conf import settings
import os
from django.contrib import messages
from predictor.models import Predictions

# Define the path to the saved model and other components
model_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'diabetes_model_with_all_features.pkl')

# Load the trained model and other necessary components
model_data = joblib.load(model_path)
model = model_data['model']
scaler = model_data['scaler']
mean_hba1c = model_data['mean_hba1c']
label_encoders = model_data['label_encoders']

@login_required
def predict_diabetes(request):
    if request.method == 'POST':
        # Get form data
        gender = request.POST.get('gender')
        age = int(request.POST.get('age'))
        hypertension = int(request.POST.get('hypertension'))
        heart_disease = int(request.POST.get('heart_disease'))
        smoking_history = request.POST.get('smoking_history')
        bmi = float(request.POST.get('bmi'))
        blood_glucose_level = float(request.POST.get('blood_glucose_level'))
        hba1c_level = request.POST.get('HbA1c_level')

        # Handle optional HbA1c level
        hba1c_level = float(hba1c_level) if hba1c_level else mean_hba1c

        # Encoding categorical variables
        gender_encoded = label_encoders['gender'].transform([gender])[0]
        smoking_history_encoded = label_encoders['smoking_history'].transform([smoking_history])[0]

        # Prepare the feature array for prediction as DataFrame
        features = pd.DataFrame([[
            gender_encoded,
            age,
            hypertension,
            heart_disease,
            smoking_history_encoded,
            bmi,
            hba1c_level,
            blood_glucose_level
        ]], columns=['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level'])

        # Scale the features
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features_scaled)
        result = "You are at the risk of Diabetes" if prediction[0] == 1 else "You are Not at the risk of Diabetes"
        
        # Saving Prediction in Database
        Predictions.objects.create(
            user = request.user,
            gender = gender,
            age = age,
            hypertension = hypertension,
            heart_disease = heart_disease,
            smoking_history = smoking_history,
            bmi = bmi,
            hba1c_level = hba1c_level,
            blood_glucose_level = blood_glucose_level,
            prediction_result = result
        )
        return render(request, 'result.html', {'result': result})
    return render(request, 'prediction.html')

@login_required
def clear_prediction(request):
    if request.method == 'POST':
        if Predictions.objects.filter(user=request.user).exists():
            Predictions.objects.filter(user=request.user).delete()
            messages.info(request, 'Predictions Have been Cleared')
        else:
            messages.info(request, 'No predictions to clear.')
    return redirect('index')