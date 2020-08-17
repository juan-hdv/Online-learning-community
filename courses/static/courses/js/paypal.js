/**
  Paypal front 
  from: https://www.paypal.com/apex/product-profile/ordersv2/approveOrder

  WARNING - READ THIS ALSO: 
  https://developer.paypal.com/docs/checkout/reference/upgrade-integration/#6-fix-deprecations
  as for the return and cancel urls
  */
var LOCAL_SERVER = "http://127.0.0.1:8000";
var internal_orderid = "{{ o.id }}";
paypal.Buttons({
    env: 'sandbox', /* sandbox | production */
    style: {
                layout: 'horizontal',   // horizontal | vertical 
                size:   'responsive',   /* medium | large | responsive*/
                shape:  'pill',         /* pill | rect*/
                color:  'gold',         /* gold | blue | silver | black*/
                fundingicons: false,    /* true | false */
                tagline: false          /* true | false */
            }, 
 
    /* createOrder() is called when the button is clicked */
    createOrder: function() {
          /* Set up a url on your server to create the order */
          var CREATE_URL = '/dopayment';
          /* Make a call to your server to set up the payment */
          return fetch(CREATE_URL, {
            method: 'POST',
            headers: { 
              'X-CSRFToken': csrftoken, // Indispensable!!!!!
              'Accept': "application/json",
              'Content-Type': "application/json",
              'accept-language': "en_US",
              'dataType': 'json',
            },
            body: JSON.stringify ({
              orderid: internal_orderid,
            }),
          }).then(function(res) {
            return res.json();
          }).then(function(data) {
            // return data.id
            return data.id;
          }).catch(function(error) {
            console.log("Error createOrder", error);
          });
     },
  
    /* onApprove() is called when the buyer approves the payment */
    onApprove: function(data, actions) {
         /* Set up a url on your server to execute the payment */
         var EXECUTE_URL = '/capturepayment';
         var COMPLETE_URL = '/showpayment';
 
        /* Set up the data you need to pass to your server */
 
        /* Make a call to your server to execute the payment */
        return fetch(EXECUTE_URL, {
            method: 'POST',
            headers: { 
              'X-CSRFToken': csrftoken, // Indispensable!!!!!
            },
            body: JSON.stringify ({
              orderID: data.id
            }),
        }).then(function(res) {
          return res.json();
        }).then(function(details) {
          // alert ("Senquiu: "+details.payer.name.surname);
          actions.redirect(LOCAL_SERVER+COMPLETE_URL);
          return true;
        }).catch(function(error) {
          console.log("Error onApprove", error);
        });
  },
  onCancel: function(data, actions) {
    var CANCEL_URL = '/cancelpayment';
    actions.redirect(LOCAL_SERVER+CANCEL_URL);
    return false;
  },
  onError: function() {
    alert ("An error has occurred. Please try again.");
    return false;
  }
}).render('#paypal-button-container-{{ o.id }}');