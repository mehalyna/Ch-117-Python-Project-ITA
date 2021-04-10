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

/* Here you can add more inputs to set value. if it's saved */
let search = document.getElementById("searchInput");
search.value = getSavedValue("searchInput");
document.getElementById("searchReset").addEventListener("click", () =>{
    localStorage.clear();
})
//Save the value function - save it to localStorage as (ID, VALUE)
function saveValue(e) {
    var id = e.id;  // get the sender's id to save it .
    var val = e.value; // get the value.
    localStorage.setItem(id, val);// Every time user writing something, the localStorage's value will override .
}

//get the saved value function - return the value of "v" from localStorage.
function getSavedValue(v) {
    if (!localStorage.getItem(v)) {
        return "";// You can change this to your defualt value.
    }
    return localStorage.getItem(v);
}
