'use strict'

const top_swiper = new Swiper('.first-container', {
  // Optional parameters
  direction: 'horizontal',
  loop: true,

  // Navigation arrows
  navigation: {
    nextEl: '.first-next',
    prevEl: '.first-prev',
  },

  slidesPerView: 5,
  spaceBetween: 20,
  speed: 600,
});


const new_slider = new Swiper('.second-container', {
  // Optional parameters
  direction: 'horizontal',
  loop: true,

  // Navigation arrows
  navigation: {
    nextEl: '.second-next',
    prevEl: '.second-prev',
  },

  slidesPerView: 5,
  spaceBetween: 20,
  speed: 600,
});

setTimeout(function () {
    if ($('#msg').length > 0) {
        $('#msg').fadeTo(500, 0, function () {})
    }
}, 2000)

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
                else if(data['message'] == "inactive"){
                    $("#errorlogin").html("Please verify this Username address.");
                }
                else{
                    $("#errorlogin").html("The Username and Password do not match.");
                }
            }
        });
    }


 function login_user(){
        let email = document.getElementById("exampleInputUsername").value;
        let password = document.getElementById("exampleInputPassword").value;
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
                    location.reload();
                }
                else if(data['message'] == "inactive"){
                    $("#errorlogin").html("Please verify this Username address.");
                }
                else{
                    $("#errorlogin").html("The Username and Password do not match.");
                }
            }
        });
    }