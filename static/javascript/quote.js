// quote.js
// javascript for handling AJAX requests on the quote page

$( document ).ready(function() {

    // get stock quotes via javascript
    $("#submitbutton").click(function(){
        event.preventDefault();
        // If input is blank, abort mission
        if($('#tickerbox').val() === "") {
            $('#error').removeClass('hidden');
            $('#stockname').html('--');
            $('#stockticker').html('--');
            $('#stockprice').html('--');
            return;
        }

        // Add spinners from font awesome during AJAX request
        var spinner = '<i class="fa fa-spinner fa-spin"></i>';
        $('#stockname').html(spinner);
        $('#stockticker').html(spinner);
        $('#stockprice').html(spinner);

        // Build API request URL from input field     
        var api_url = "/jsonquote/" + $('#tickerbox').val();

        // request stock quote and update accordingly
        $.get(api_url, function(data, status){
            // If price is 0, an error object was returned
            if (data.price === 0) {
                 $('#error').removeClass('hidden');
                 $('#stockname').html('--');
                 $('#stockticker').html('--');
                 $('#stockprice').html('--');
                 $("#tickerbox").val('');
                 return;
            }
            // otherwise we're good, remove any old error and display data
            $('#error').addClass('hidden');
            $('#stockname').html(data.name);
            $('#stockticker').html(data.ticker);
            $('#stockprice').html(currencyFormat(data.price));
            $("#tickerbox").val('');
         });
        });    
    
    
});

// currency format function adapted from https://blog.tompawlak.org/number-currency-formatting-javascript
function currencyFormat (num) {
    return "$" + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
}