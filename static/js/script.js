// JavaScript for timing restrictions on sign-up form
document.getElementById('signup-form').onsubmit = function (event) {
    const today = new Date();
    const shiftDate = new Date(document.getElementById('shift-date').value);
    const hoursBeforeOpening = new Date();
    hoursBeforeOpening.setHours(hoursBeforeOpening.getHours() - 1);

    if (shiftDate <= today || today.getDay() === 0 || today.getDay() === 6) {
        document.getElementById('signup-message').innerText = "Sign-ups are only open Mon-Fri and must be done a day in advance.";
        event.preventDefault();
    }
};

// Confirmation button availability based on current time
document.getElementById('confirm-button').onclick = function () {
    const today = new Date();
    if (today.getHours() >= 9 && today.getHours() <= 17) { // Example time range for workday shifts
        document.getElementById('confirm-message').innerText = "Attendance confirmed!";
    } else {
        document.getElementById('confirm-message').innerText = "Confirmations are only allowed during shift hours.";
    }
};
