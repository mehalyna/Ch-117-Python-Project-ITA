const passPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

let form = document.querySelector('.needs-validation');
let inputsList = form.querySelectorAll('input.form-control');


let old_password = form.elements.namedItem('old_password');
let new_password = form.elements.namedItem('new_password');
let confirmPassword = form.elements.namedItem('confirm_password');
let submitButton = form.elements.namedItem('submitButton');
submitButton.disabled = true;

old_password.addEventListener('input', validationFuncsOldPassword);
new_password.addEventListener('input', validationFuncsNewPassword);
confirmPassword.addEventListener('input', validationFuncsConfirmPassword);


function validationFuncsOldPassword() {
    validateOldPassword();
    checkFormValid();
}

function validationFuncsNewPassword() {
    validateNewPassword();
    checkFormValid();
}

function validationFuncsConfirmPassword() {
    validateConfirmPassword();
    checkFormValid();
}


function validateOldPassword() {
    validatePasswords(old_password, '#oldPasswordError');
}

function validateNewPassword() {
    validatePasswords(new_password, '#newPasswordError');
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
    } else if (new_password.value !== confirmPassword.value && new_password.value && confirmPassword.value) {
        confirmPassword.classList.add('is-invalid');
        setErrorFor('#confirmPasswordError', 'Passwords doesn\'t match');
        return false;
    } else if (new_password.value === confirmPassword.value) {
        confirmPassword.classList.remove('is-invalid');
        setSuccessFor('#confirmPasswordError');
        return true;
    } else {
        element.classList.remove('is-invalid');
        setSuccessFor(errorId);
        return true;
    }
}

function showPassword() {
  if (old_password.type === "password" && new_password.type === "password"  && confirmPassword.type === "password" ) {
    old_password.type = "text";
    new_password.type = "text";
    confirmPassword.type = "text";
  } else {
    old_password.type = "password";
    new_password.type = "password";
    confirmPassword.type = "password";
  }
}
