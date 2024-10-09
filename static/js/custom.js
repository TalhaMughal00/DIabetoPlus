
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
    if (isNaN(wtKg) || wtKg <= 0) {
        toastr.error('Please Enter a Valid Weight.', 'Error');
        return;
    }
    let tdd1 = wtKg * 0.55;
    tdd1 = Math.round(tdd1 / 2) * 2;
    document.getElementById('tdd').value = `Your TDD is: ${tdd1} Units`;
    let perMeal = tdd1 / 3;
    perMeal = Math.round(perMeal / 2) * 2;
    document.getElementById('tdd_pm').value = `Your TDD(Per Meal) is: ${perMeal} Units`;
}

function calcinsulin_cf() {
    const tddc = parseFloat(document.getElementById('tddc').value);
    const bgh = parseFloat(document.getElementById('bgh').value);
    const bgt = parseFloat(document.getElementById('bgt').value)

    if (isNaN(tddc) || isNaN(bgh) || isNaN(bgt)) {
        toastr.error('Please Enter Valid Values.', 'Error');
        return;
    }

    let cf = 1800 / tddc;
    let insulin_cf = (bgh - bgt) / cf;

    insulin_cf = Math.round(insulin_cf / 2) * 2

    document.getElementById('tddcf').value = `Your Correctoion Factor is: ${insulin_cf} Units of Rapid Action Insulin`;
}