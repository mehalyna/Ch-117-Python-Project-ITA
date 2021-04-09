function change_status(url, status) {
    const ask = window.confirm(`Are you sure you want to ${status} this user?`);
    if (ask) {
        window.location.href = url;
    }
}

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0, function (){
    })
}, 2000);
