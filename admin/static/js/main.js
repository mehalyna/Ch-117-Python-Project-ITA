function change_status(url, status) {
    const ask = window.confirm(`Are you sure you want to ${status} this user?`);
    if (ask) {
        window.location.href = url;
    }
}

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0, function (){
    })
}, 5000);

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function validateForm(formName) {
    let title = document.forms[formName]['title'].value;
    let author_name = document.forms[formName]['author_name'].value;
    let year = document.forms[formName]['year'].value;
    let language = document.forms[formName]['language'].value;

    if (title === "") {
        document.querySelector('#title').classList.add('is-invalid');
    }

      if (author_name === "") {
        document.querySelector('#author_name').classList.add('is-invalid');
    }

    if (year === "") {
        document.querySelector('#year').classList.add('is-invalid');
    }

    if (language === "") {
        document.querySelector('#language').classList.add('is-invalid');
    }

    if (author_name === '' || title === '' || year === '' || language === '') {
        return false
    }
}
