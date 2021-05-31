function paymentMethod(stripePublicKey, url) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Create an instance of the Stripe object with your publishable API key
    var stripe = Stripe(stripePublicKey);
    var checkoutButton = document.getElementById("checkout-button");
    var paymentId = document.querySelector('input[name = price]:checked').value;
    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({paymentId: paymentId})
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
