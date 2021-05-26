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
email.addEventListener('blur', validateUnique);
username.addEventListener('input', validationFuncsUsername);
username.addEventListener('blur', validateUnique);

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

function validateUnique(e) {
    const errorSuffix = 'Error';
    let element = e.target;
    let errorId = '#' + element.name + errorSuffix;
    let validateUrl = `/library/edit_profile_unique_validation/`;
    let csrftoken = getCookie('csrftoken');
    const request = new Request(
        validateUrl,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        body: JSON.stringify({field_value: element.value}),
        method: 'POST',
    }).then(response => response.json()).then(data => {
        if (data.error_message) {
            element.classList.add('is-invalid');
            setErrorFor(errorId, data.error_message);
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
