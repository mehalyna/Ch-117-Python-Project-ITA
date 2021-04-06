function change_status(url, status) {
    const ask = window.confirm(`Are you sure you want to ${status} this user?`);
    if (ask) {
        window.location.href = url;
    }
}

$(document).ready(function () {
    $("#myInput").on("keyup", function () {
        let value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});


window.setTimeout(function() {
    $(".alert").fadeTo(500, 0, function (){
      $(this)[0].style.display = 'none'
    })
}, 2000);


$(document).ready(function(){
  $("#mySearch").on("keyup", function() {
    let value = $(this).val().toLowerCase();
    $("#bookTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
