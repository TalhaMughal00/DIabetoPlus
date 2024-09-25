// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}
getYear();

// Logging Welcome Message
setTimeout(function () {
    document.querySelector(".message").classList.add("fade-out");
    document.querySelector(".message").style.display = "none";
}, 5000); // hide the message after 6 seconds


// BMI Calculator
function calculateBMI() {
    const heightFeet = parseFloat(document.getElementById('height').value);
    const weightKg = parseFloat(document.getElementById('weight').value);

    if (isNaN(heightFeet) || isNaN(weightKg) || heightFeet <= 0 || weightKg <= 0) {
        document.getElementById('result').innerText = 'Please enter valid numbers.';
        return;
    }

    const heightMeters = heightFeet * 0.3048;
    const bmi = weightKg / (heightMeters * heightMeters);
    const bmiRounded = bmi.toFixed(2);

    document.getElementById('result').innerText = `Your BMI is ${bmiRounded}`;
}