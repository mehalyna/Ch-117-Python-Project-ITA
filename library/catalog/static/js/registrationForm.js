const emailPattern = /^(\w|\.|_|-)+[@](\w|_|-|\.)+[.]\w{2,3}$/;
const passPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

let form = document.querySelector('.needs-validation');
let inputsList = document.querySelectorAll('input.form-control');

let firstname = form.elements.namedItem('firstname');
let lastname = form.elements.namedItem('lastname');
let email = form.elements.namedItem('email');
let login = form.elements.namedItem('login');
let password = form.elements.namedItem('password');
let confirmPassword = form.elements.namedItem('confirm_password');
let submitButton = form.elements.namedItem('submitButton');

firstname.addEventListener('input', validateFirstname);
firstname.addEventListener('input', checkFormValid);
lastname.addEventListener('input', validateLastname);
lastname.addEventListener('input', checkFormValid);
email.addEventListener('input', validateEmail);
email.addEventListener('input', checkFormValid);
login.addEventListener('input', validateLogin);
login.addEventListener('input', checkFormValid);
password.addEventListener('input', validatePassword);
password.addEventListener('input', checkFormValid);
confirmPassword.addEventListener('input', validateConfirmPassword);
confirmPassword.addEventListener('input', checkFormValid);


function validateFirstname() {
    dataRequired(firstname, '#firstnameError');
}

function validateLastname() {
    dataRequired(lastname, '#lastnameError');
}

function validateEmail() {
    let errorId = '#emailError';

    if (!dataRequired(email, errorId)) {
    } else if (!emailPattern.test(email.value)) {
        email.classList.add('is-invalid');
        setErrorFor(errorId, 'Invalid email');
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
    } else if (!validateUnique(login, errorId)) {
    } else {
        login.classList.remove('is-invalid');
        setSuccessFor(errorId);
    }
}

function validatePassword(){
    validatePasswords(password, '#passwordError');
}

function validateConfirmPassword(){
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
    if (element.value === '') {
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
