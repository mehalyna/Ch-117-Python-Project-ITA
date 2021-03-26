function deleteUser(_id) {
    var ask = window.confirm(`Are you sure you want to delete this user?`);
    if (ask) {
        window.location.href = `/delete/${_id}`;
    }
}
function createUser() {
    var ask = window.confirm(`Are you sure you want to create this user?`);
    if (ask) {
        window.location.href = `/create_user    `;
    }
}
