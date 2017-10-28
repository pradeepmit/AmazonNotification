$(function() {
    $('#SearchProduct').click(function() {
        alert("We are fetching products for you Please Pay patience...");
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                console.log('---',$('#ProductList'));
                $('#ProductList')[0].innerHTML = response;
            },
            error: function(error) {
                console.log(error);
                alert("Something went wrong");
            }
        });
    });
});

$(function(){
    $("#subscriptionBtn").click(function(){
        $.ajax({
            url: '/saveEmailNProduct',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                alert("Successsfully Subscribed");
                
            },
            error: function(error) {
                console.log(error);
                alert("Something went wrong");
            }
        });

    });
});