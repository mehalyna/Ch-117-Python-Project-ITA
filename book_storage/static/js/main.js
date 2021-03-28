function deleteUser(url) {
    const ask = window.confirm(`Are you sure you want to delete this user?`);
    if (ask) {
        window.location.href = url;
    }
}
