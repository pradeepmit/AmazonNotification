$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                var response = JSON.parse(response);
               $('#signedURL').text(response['signedurl']);
               $('#signedURL').attr('href',response['signedurl']);


            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});