function change_status(url, status) {
    const ask = window.confirm(`Are you sure you want to ${status} this user?`);
    if (ask) {
        window.location.href = url;
    }
}

window.setTimeout(function () {
    $(".alert").fadeTo(500, 0, function () {
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

function saveValue(e) {
    var id = e.id;
    var val = e.value;
    localStorage.setItem(id, val);
}

function getSavedValue(v) {
    if (!localStorage.getItem(v)) {
        return "";
    }
    return localStorage.getItem(v);
}

(() => {
    'use strict';
    const paths_names = ['users_list', 'active_users_list', 'inactive_users_list', 'update_user'];
    let search = document.getElementById('userSearch');
    let reset = document.getElementById('searchReset');
    if (search){
        search.value = getSavedValue('userSearch');
    }
        if (reset){
            reset.addEventListener('click', () => {
            localStorage.removeItem('userSearch');
        })
        }

    if (!paths_names.includes(window.location.pathname.split('/')[1])) {
        localStorage.removeItem('userSearch');
    }
})();

(() => {
    'use strict';
    let edit_button_list = document.querySelectorAll('.update_user');
    edit_button_list.forEach(button =>{button.addEventListener('click', (event) => {
        localStorage.removeItem('back_to_url');
        localStorage.setItem('back_to_url', window.location);
    }, false);
    })
})();

function back_to_user(){
    window.location.href = localStorage.getItem('back_to_url');
}
