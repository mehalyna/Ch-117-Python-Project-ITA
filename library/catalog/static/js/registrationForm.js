const emailPattern = /^(\w|\.|_|-)+[@](\w|_|-|\.)+[.]\w{2,3}$/
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

firstname.addEventListener('input', validate);
lastname.addEventListener('input', validate);
email.addEventListener('input', validate);
password.addEventListener('input', validate);
confirmPassword.addEventListener('input', validate);
login.addEventListener('input', validate);


function validate(e) {
    let target = e.target;
    dataRequired(target);
    if (target.name === 'email') {
        if (!emailPattern.test(target.value)) {
            target.classList.add('is-invalid');
            setErrorFor(target, 'Invalid email');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(target)
        }

    }
    else if (target.name === 'login') {
        if (target.value.length < 6) {
            target.classList.add('is-invalid');
            setErrorFor(target, 'Minimum 6 characters long');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(target)
        }
    }
    else if (target.name === 'password' || target.name === 'confirm_password') {
        validatePasswords(target);
    }

    checkFormValid(inputsList);
}


function setErrorFor(input, message) {
    let formControl = input.parentElement.parentElement;
    let small = formControl.querySelector('small');

    small.innerText = message;
    small.style.visibility = 'visible';
    submitButton.disabled = true;
}

function setSuccessFor(input) {
    let formControl = input.parentElement.parentElement;
    let small = formControl.querySelector('small');

    small.style.visibility = 'hidden';
}

function checkFormValid(inputsList) {
    let valueInputsList = []
    let classInputsList = []
    for (let input of inputsList) {
        classInputsList = classInputsList.concat(input.classList.value.split(' '));
        valueInputsList.push(input.value);
    }
    if (valueInputsList.includes('')) {
        submitButton.disabled = true;
    } else if (!classInputsList.includes('is-invalid')) {
        submitButton.disabled = false;
    }
}

function dataRequired(element) {
    if (element.value === '') {
        element.classList.add('is-invalid');
        setErrorFor(element, 'This field is required.');
    } else {
        element.classList.remove('is-invalid');
        setSuccessFor(element)
    }
}

function validatePasswords(element) {
    if (!passPattern.test(element.value)) {
        element.classList.add('is-invalid');
        setErrorFor(element, 'Minimum 8 characters, at least 1 letter and 1 number');
    } else {
        element.classList.remove('is-invalid');
        setSuccessFor(element)
    }
}