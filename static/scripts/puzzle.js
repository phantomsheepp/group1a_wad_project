/*var button = document.getElementById("submit-button");
button.addEventListener("click", showOptions);

function showOptions() {
    print("hi");
    document.getElementById("guess-title").style.BackgroundColor = "green";
}
*/

var maxGuesses = 3;

let count = 0;

function finished(success, count) {
    $.post('/bookle/save-score', {'success':success, 'count':count}, function(data) {
        // 
    });
    window.location.replace(window.location.href+"complete");
}


// JQuery
$(document).ready(function() {
    console.log("{{ puzzleDate }}");
    $("#guessCount").text(maxGuesses + " guesses left");

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
            // need to be able to access data as well as page
            //var success = data['success']
        });
        

        
        count++;
        if (count >= maxGuesses) {
            finished(false, count);
            /*$.get('/bookle/puzzle/daily/complete', {'count':count}, function(data) {
                //$("#completeGuesses").text("hello");
                // $("#finalGuessCount").text(JSON.parse(data)["count"]);
                //window.location.replace(window.location.href+"complete");
            });*/
        }

        $("#guessCount").text((maxGuesses-count) + " guesses left");
    });
});