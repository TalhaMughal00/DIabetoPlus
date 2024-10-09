
// BMI Calculator
function calculateBMI() {
    const heightFeet = parseFloat(document.getElementById('heightFeet').value);
    const heightInches = parseFloat(document.getElementById('heightInches').value);
    const weightKg = parseFloat(document.getElementById('weight').value);

    // Validate input
    if (isNaN(heightFeet) || isNaN(heightInches) || isNaN(weightKg) || heightFeet <= 0 || heightInches < 0 || weightKg <= 0) {
        document.getElementById('result').innerText = 'Please Enter Valid Numbers.';
        return;
    }

    // Convert height from feet and inches to meters
    const totalInches = (heightFeet * 12) + heightInches;
    const heightMeters = totalInches * 0.0254;

    // Calculate BMI
    const bmi = weightKg / (heightMeters * heightMeters);
    const bmiRounded = bmi.toFixed(2);

    // Determine BMI category
    let category;
    if (bmi < 18.5) {
        category = 'Underweight';
    } else if (bmi >= 18.5 && bmi < 25) {
        category = 'Normal weight';
    } else if (bmi >= 25 && bmi < 30) {
        category = 'Overweight';
    } else if (bmi >= 30 && bmi < 35) {
        category = 'Obesity Class I (Moderate)';
    } else if (bmi >= 35 && bmi < 40) {
        category = 'Obesity Class II (Severe)';
    } else {
        category = 'Obesity Class III (Very Severe or Morbid)';
    }

    // Display result
    document.getElementById('result').innerText = `Your BMI is ${bmiRounded} (${category})`;
}
function calcinsulin() {
    const wtKg = parseFloat(document.getElementById('weightkg').value);

    // Validate input
    if (isNaN(wtKg) || wtKg <= 0) {
        document.getElementById('tdd').innerText = 'Please Enter Valid Weight.';
        return;
    }

    const tdd1 = wtKg * 0.55;

    document.getElementById('tdd').innerText = `Your Total Daily Dose (TDD) is ${tdd1.toFixed(2)} units`;
}