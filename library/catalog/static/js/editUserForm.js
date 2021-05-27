const profanityRegexp = /(\w?\d?)(ass|bastard|bitch|bollocks|boobs|bottom|bugger|clunge|cock|cunt|damn|dick|fuck|gash|knob|minge|motherfucker|piss off|prick|punani|pussy|shit|snatch|suck|tits|twat|wanker)(\w?\d?)/gi;
const emailPattern = /^(\w|\.|_|-)+[@](\w|_|-|\.)+[.]\w{2,3}$/;

let form = document.querySelector('.needs-validation');
let inputsList = form.querySelectorAll('input.form-control');

let firstname = form.elements.namedItem('firstname');
let lastname = form.elements.namedItem('lastname');
let email = form.elements.namedItem('email');
let username = form.elements.namedItem('username');

let submitButton = form.elements.namedItem('submitButton');

firstname.addEventListener('input', validationFuncsFirstname);
lastname.addEventListener('input', validationFuncsLastname);
email.addEventListener('input', validationFuncsEmail);
username.addEventListener('input', validationFuncsUsername);

function validationFuncsFirstname() {
    validateFirstname();
    checkFormValid();
}

function validationFuncsLastname() {
    validateLastname();
    checkFormValid();
}

function validationFuncsEmail() {
    validateEmail();
    checkFormValid();
}

function validationFuncsUsername() {
    validateUsername();
    checkFormValid();
}

function validateFirstname() {
    let errorId = '#firstnameError';
    if (!dataRequired(firstname, errorId)) {
    } else if (!validateProfanity(firstname, errorId)) {
    }
}

function validateLastname() {
    let errorId = '#lastnameError';
    if (!dataRequired(lastname, errorId)) {
    } else if (!validateProfanity(lastname, errorId)) {
    }
}

function validateEmail() {
    let errorId = '#emailError';

    if (!dataRequired(email, errorId)) {
    } else if (!emailPattern.test(email.value)) {
        email.classList.add('is-invalid');
        setErrorFor(errorId, 'Invalid email');
    } else if (!validateProfanity(email, errorId)) {
    } else if (!validateUnique(email, errorId)) {
    } else {
        email.classList.remove('is-invalid');
        setSuccessFor(errorId);
    }
}

function validateUsername() {
    let errorId = '#usernameError'

    if (!dataRequired(username, errorId)) {
    } else if (username.value.length < 6) {
        username.classList.add('is-invalid');
        setErrorFor(errorId, 'Minimum 6 characters long');
    } else if (!validateProfanity(username, errorId)) {
    } else if (!validateUnique(username, errorId)) {
    } else {
        username.classList.remove('is-invalid');
        setSuccessFor(errorId);
    }
}


function setErrorFor(errorId, message) {
    let validationError = document.querySelector(errorId);

    validationError.innerText = message;
    validationError.style.visibility = 'visible';
    submitButton.disabled = true;
}

function setSuccessFor(errorId) {
    let validationError = document.querySelector(errorId);
    validationError.style.visibility = 'hidden';
}

function checkFormValid() {
    let valueInputsList = [];
    let classInputsList = [];

    inputsList.forEach(input => {
        classInputsList = classInputsList.concat(input.classList.value.split(' '));
        valueInputsList.push(input.value);
    })
    if (valueInputsList.includes('')) {
        submitButton.disabled = true;
    } else if (!classInputsList.includes('is-invalid')) {
        submitButton.disabled = false;
    }
}

function dataRequired(element, errorId) {
    if (element.value.trim() === '') {
        element.classList.add('is-invalid');
        setErrorFor(errorId, 'This field is required');
        return false;
    } else {
        element.classList.remove('is-invalid');
        setSuccessFor(errorId);
        return true;
    }
}


function validateUnique(element, errorId) {
    let validationText = '';
    let validateUrl = `/library/edit_profile_validation/${element.value}`;
    let request = new XMLHttpRequest();
    request.open("GET", validateUrl, false);
    request.send(null);
    if (request.readyState === 4 && request.status === 200) {
        validationText = request.responseText;
    }
    if (validationText) {
        element.classList.add('is-invalid');
        setErrorFor(errorId, validationText);
        return false;
    } else {
        element.classList.remove('is-invalid');
        setSuccessFor(errorId);
        return true;
    }
}


function validateProfanity(element, errorId) {
    if (!element.value.search(profanityRegexp)) {
        element.classList.add('is-invalid');
        setErrorFor(errorId, 'This field contains profanity');
        return false;
    } else {
        element.classList.remove('is-invalid');
        setSuccessFor(errorId);
        return true;
    }
}
