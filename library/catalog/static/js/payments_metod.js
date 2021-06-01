let inputField = document.getElementById("customPriceInput");
let radioButtonList = document.querySelectorAll("input[name=price]");
radioButtonList.forEach(radioButton => {
    radioButton.addEventListener('click', function (){
        inputField.disabled = radioButton.id !== 'customPrice';
    })
})

function paymentMethod(stripePublicKey, url) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var stripe = Stripe(stripePublicKey);
    var checkedPrice = document.querySelector('input[name = price]:checked');
    let unit_amount;
    if (checkedPrice.id === "customPrice"){
        unit_amount = inputField.value * 100;
    }
    else {
        unit_amount = checkedPrice.value;
    }
    if (!isNaN(unit_amount)){
        fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({unit_amount: parseInt(unit_amount)})
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (session) {
            return stripe.redirectToCheckout({sessionId: session.id});
        })
        .then(function (result) {
            if (result.error) {
                alert(result.error.message);
            }
        })
        .catch(function (error) {
            console.error("Error:", error);
        });
    }
    else {
        alert('Input correct amount')
    }

}
