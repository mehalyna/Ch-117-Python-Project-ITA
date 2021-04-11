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
