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
    const paths_names = ['book-storage', 'book-active', 'book-inactive', 'book-update'];
    let search = document.getElementById('bookSearch');
    let reset = document.getElementById('searchReset');
    if (search) {
        search.value = getSavedValue('bookSearch');
    }
    if (reset) {
        reset.addEventListener('click', () => {
            localStorage.removeItem('bookSearch');
        })
    }

    if (!paths_names.includes(window.location.pathname.split('/')[1])) {
        localStorage.removeItem('bookSearch');
    }
})();

(() => {
    'use strict';
    let edit_button_list = document.querySelectorAll('.save_url');
    edit_button_list.forEach(button => {
        button.addEventListener('click', (event) => {
            localStorage.removeItem('back_to_url');
            localStorage.setItem('back_to_url', window.location);
        }, false);
    })
})();

function back_to_list() {
    window.location.href = localStorage.getItem('back_to_url');
}
