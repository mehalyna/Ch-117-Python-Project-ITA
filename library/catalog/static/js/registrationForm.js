let form = document.querySelector('.needs-validation');

let firstname = form.elements.namedItem('firstname');
let lastname = form.elements.namedItem('lastname');
let email = form.elements.namedItem('email');
let login = form.elements.namedItem('login');
let password = form.elements.namedItem('password');
let confirmPassword = form.elements.namedItem('confirm_password');
let button = form.elements.namedItem('');

firstname.addEventListener('input', validate);
lastname.addEventListener('input', validate);
email.addEventListener('input', validate);
password.addEventListener('input', validate);
confirmPassword.addEventListener('input', validate);
login.addEventListener('input', validate);


function validate(e) {
    let target = e.target;

    if (target.name === 'firstname') {
        if (target.value === '') {
            target.classList.add('is-invalid');
            setErrorFor(firstname, 'This field is required.');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(firstname)
        }
    }
    if (target.name === 'lastname') {
        if (target.value === '') {
            target.classList.add('is-invalid');
            setErrorFor(lastname, 'This field is required.');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(lastname)
        }
    }
    if (target.name === 'email') {
        if (target.value === '') {
            target.classList.add('is-invalid');
            setErrorFor(email, 'This field is required.');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(email)
        }
    }
    if (target.name === 'login') {
        if (target.value === '') {
            target.classList.add('is-invalid');
            setErrorFor(login, 'This field is required.');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(login)
        }
    }
    if (target.name === 'password') {
        if (target.value === '') {
            target.classList.add('is-invalid');
            setErrorFor(password, 'This field is required.');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(password)
        }
    }
    if (target.name === 'confirm_password') {
        if (target.value === '') {
            target.classList.add('is-invalid');
            setErrorFor(confirmPassword, 'This field is required.');
        } else {
            target.classList.remove('is-invalid');
            setSuccessFor(confirmPassword)
        }
    }
}


function setErrorFor(input, message) {
    let formControl = input.parentElement.parentElement;
    let small = formControl.querySelector('small');

    small.innerText = message;
    small.style.visibility = 'visible';
}

function setSuccessFor(input) {
    let formControl = input.parentElement.parentElement;
    let small = formControl.querySelector('small');

    small.style.visibility = 'hidden';
}