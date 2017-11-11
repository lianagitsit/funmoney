// sell.js
// javascript for handling AJAX on the sell page
// Displays total transaction value before sell happens

$( document ).ready(function() {
    // console.log("linked!");
    $('#sellticker').keyup(function(event) {
        //console.log($(this).val());
        total();
    });

    $('#sellshares').keyup(function(event) {
        //console.log($(this).val());
        total();
    });

});

function total() {
    var spinner = '<i class="fa fa-spinner fa-spin"></i>';
    $('#transvalue').html(spinner);
    if ($('#sellticker').val() === "" || $('#sellshares').val() == "") {
        //console.log("exiting total!");
        return;
    }

    // prepare the URL for the API call
    var api_url = "/jsonquote/" + $('#sellticker').val();
    //console.log("Querying URL!");
     // request stock quote and update accordingly
    $.get(api_url, function(data, status){
            // If price is 0, an error object was returned, abort
            if (data.price === 0) {
                // console.log("Got an error asking for a price");
                 return;
            }
            //console.log("Got a quote!");
            //console.log(data);
            // Since we got a quote, render tx value
            // hack to parse an int
            var shares = +$('#sellshares').val();
            var price = data.price;
            $('#transvalue').html(currencyFormat(shares * price));
            $('#sellbutton').prop('disabled', false);
           
         }); 

    
}

// TODO: Use imports or something here, duplicated javascript!
// currency format function adapted from https://blog.tompawlak.org/number-currency-formatting-javascript
function currencyFormat (num) {
    return "$" + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
}