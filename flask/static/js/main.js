function deleteUser(url) {
    const ask = window.confirm(`Are you sure you want to delete this user?`);
    if (ask) {
        window.location.href = url;
    }
}
function createUser() {
    const ask = window.confirm(`Are you sure you want to create this user?`);
    if (ask) {
        window.location.href = `/create_user`;
    }
}
