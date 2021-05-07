$(window).on('load', function() {
    $('#authModal').modal('show');
});


function combinedСallUsername(){
    validateCredentials();
    usernameErrorMessage();
}

function combinedСallPassword(){
    validateCredentials();
    passwordErrorMessage();
}

function validateCredentials(){
  var first = document.getElementById('inputUsername').value.length;
  var second = document.getElementById('inputPassword').value.length;

  if(first > 5 && second > 7){
    document.getElementById('submitButton').disabled=false;
  } else {
    document.getElementById('submitButton').disabled=true;
  }
}

function usernameErrorMessage(){
  var inputLogin = document.getElementById('inputUsername').value.length;

  if(inputLogin < 6){
    $("#errorUsername").html("Minimum 6 characters").css('color', 'red');
  } else {
  $("#errorUsername").html("  ");
  }
}

function passwordErrorMessage(){
  var inputPassword = document.getElementById('inputPassword').value.length;

  if(inputPassword < 8){
    $("#errorPassword").html("Minimum 8 characters").css('color', 'red');
  } else {
  $("#errorPassword").html("  ");
  }
}

function login_user_redirect(){
        let email = document.getElementById("inputUsername").value;
        let password = document.getElementById("inputPassword").value;
        let redirect_page = document.getElementById("nextPage").value;
        let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        $("#errorlogin").html("");
        $.ajax({
            type:"POST",
            url:'/library/func_login',
            data:{
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'username':email,
                'password':password,
            },
            success : function(data){
                if(data['message'] == "Success"){
                    window.location.replace(redirect_page);
                }
                else if(data['message'] == "Denied"){
                    $("#errorlogin").html("Invalid Username or Password");
                }
            }
        });
    }