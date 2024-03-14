/*var button = document.getElementById("submit-button");
button.addEventListener("click", showOptions);

function showOptions() {
    print("hi");
    document.getElementById("guess-title").style.BackgroundColor = "green";
}
*/

let count = 8


// JQuery
$(document).ready(function() {
    $("#guessCount").text(count + " guesses left");

    $("#guessInput").keyup(function() {
        var guess = $(this).val();
        $.get('/bookle/suggestions', {'guess': guess}, function(data) {
            $("#options").html(data);
        });
    });

    /*$("li").click(function() {
        alert($(this).text());
    }); */

    $("#submitButton").click(function() {
        var guess = $("#guessInput").val();
        $.get('/bookle/check-guess', {'guess': guess, 'count':count}, function(data) {
            $("#guessResults").prepend(data);
        });
        
        count -= 1;
        if (count == 0) {
            $.get('bookle/complete', {'count':count}, function(data) {

            });
        }

        $("#guessCount").text(count + " guesses left");
    });
});