// buy.js
// javascript for handling AJAX on the buy page

$( document ).ready(function() {
    // console.log("linked!");
    $('#buyticker').keyup(function(event) {
        //console.log($(this).val());
        total();
    });

    $('#buyshares').keyup(function(event) {
        //console.log($(this).val());
        total();
    });

});

function total() {
    var spinner = '<i class="fa fa-spinner fa-spin"></i>';
    $('#transvalue').html(spinner);
    if ($('#buyticker').val() === "" || $('#buyshares').val() == "") {
        //console.log("exiting total!");
        return;
    }

    // prepare the URL for the API call
    var api_url = "/jsonquote/" + $('#buyticker').val();
    //console.log("Querying URL!");
     // request stock quote and update accordingly
    $.get(api_url, function(data, status){
            // If price is 0, an error object was returned, abort
            if (data.price === 0) {
                console.log("Got an error asking for a price");
                 return;
            }
            //console.log("Got a quote!");
            //console.log(data);
            // Since we got a quote, render tx value
            // hack to parse an int
            var shares = +$('#buyshares').val();
            var price = data.price;
            $('#transvalue').html(currencyFormat(shares * price));
            $('#buybutton').prop('disabled', false);
           
         }); 

    
}

// TODO: Use imports or something here, duplicated javascript! Bad! D.R.Y. more!
// currency format function adapted from https://blog.tompawlak.org/number-currency-formatting-javascript
function currencyFormat (num) {
    return "$" + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
}