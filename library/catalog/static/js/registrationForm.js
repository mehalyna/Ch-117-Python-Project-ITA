const profanityRegexp = /(\w?\d?)(ass|bastard|bitch|bollocks|boobs|bottom|bugger|clunge|cock|cunt|damn|dick|fuck|gash|knob|minge|motherfucker|piss off|prick|punani|pussy|shit|snatch|suck|tits|twat|wanker)(\w?\d?)/gi;
const emailPattern = /^(\w|\.|_|-)+[@](\w|_|-|\.)+[.]\w{2,3}$/;
const passPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
const timeToLiveMin = 10;
const storageKeyPrefix = 'registration_';

let form = document.querySelector('.needs-validation');
let inputsList = form.querySelectorAll('input.form-control');

let firstname = form.elements.namedItem('firstname');
firstname.value = getWithExpiry(storageKeyPrefix + firstname.id);
let lastname = form.elements.namedItem('lastname');
lastname.value = getWithExpiry(storageKeyPrefix + lastname.id);
let email = form.elements.namedItem('email');
email.value = getWithExpiry(storageKeyPrefix + email.id);
let login = form.elements.namedItem('login');
login.value = getWithExpiry(storageKeyPrefix + login.id);

let password = form.elements.namedItem('password');
let confirmPassword = form.elements.namedItem('confirm_password');
let submitButton = form.elements.namedItem('submitButton');
window.onload = function (event) {
    if (firstname.value) {
        validateFirstname();
    }
    if (lastname.value) {
        validateLastname();
    }
    if (email.value) {
        validateEmail();
    }
    if (login.value) {
        validateLogin();
    }
}

firstname.addEventListener('input', validationFuncsFirstname);
lastname.addEventListener('input', validationFuncsLastname);
email.addEventListener('input', validationFuncsEmail);
login.addEventListener('input', validationFuncsLogin);
password.addEventListener('input', validationFuncsPassword);
confirmPassword.addEventListener('input', validationFuncsConfirmPassword);

function validationFuncsFirstname() {
    setWithExpiry(storageKeyPrefix + firstname.id, firstname.value, timeToLiveMin);
    validateFirstname();
    checkFormValid();
}

function validationFuncsLastname() {
    setWithExpiry(storageKeyPrefix + lastname.id, lastname.value, timeToLiveMin);
    validateLastname();
    checkFormValid();
}

function validationFuncsEmail() {
    setWithExpiry(storageKeyPrefix + email.id, email.value, timeToLiveMin);
    validateEmail();
    checkFormValid();
}

function validationFuncsLogin() {
    setWithExpiry(storageKeyPrefix + login.id, login.value, timeToLiveMin);
    validateLogin();
    checkFormValid();
}

function validationFuncsPassword() {
    validatePassword();
    checkFormValid();
}

function validationFuncsConfirmPassword() {
    validateConfirmPassword();
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

function validateLogin() {
    let errorId = '#loginError'

    if (!dataRequired(login, errorId)) {
    } else if (login.value.length < 6) {
        login.classList.add('is-invalid');
        setErrorFor(errorId, 'Minimum 6 characters long');
    } else if (!validateProfanity(login, errorId)) {
    } else if (!validateUnique(login, errorId)) {
    } else {
        login.classList.remove('is-invalid');
        setSuccessFor(errorId);
    }
}

function validatePassword() {
    validatePasswords(password, '#passwordError');
}

function validateConfirmPassword() {
    validatePasswords(confirmPassword, '#confirmPasswordError');
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


function validatePasswords(element, errorId) {
    if (!dataRequired(element, errorId)) {

    } else if (!passPattern.test(element.value)) {
        element.classList.add('is-invalid');
        setErrorFor(errorId, 'Minimum 8 characters, at least 1 letter and 1 number');
        return false;
    } else if (password.value !== confirmPassword.value && password.value && confirmPassword.value) {
        confirmPassword.classList.add('is-invalid');
        setErrorFor('#confirmPasswordError', 'Passwords doesn\'t match');
        return false;
    } else if (password.value === confirmPassword.value) {
        confirmPassword.classList.remove('is-invalid');
        setSuccessFor('#confirmPasswordError');
        return true;
    } else {
        element.classList.remove('is-invalid');
        setSuccessFor(errorId);
        return true;
    }
}

function validateUnique(element, errorId) {
    let validationText = '';
    let validateUrl = `/library/registration_validation/${element.value}`;
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

function setWithExpiry(key, value, ttl) {
    let now = new Date()

    // `item` is an object which contains the original value
    // as well as the time when it's supposed to expire
    let item = {
        value: value,
        expiry: now.getTime() + ttl * 60000,
    }
    localStorage.setItem(key, JSON.stringify(item))
}

function getWithExpiry(key) {
    const itemStr = localStorage.getItem(key)
    // if the item doesn't exist, return null
    if (!itemStr) {
        return null
    }
    let item = JSON.parse(itemStr)
    let now = new Date()
    // compare the expiry time of the item with the current time
    if (now.getTime() > item.expiry) {
        // If the item is expired, delete the item from storage
        // and return null
        localStorage.removeItem(key)
        return null
    }
    return item.value
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
