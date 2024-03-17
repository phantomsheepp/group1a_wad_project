var maxGuesses = 3;
let count = 0;
var data = document.currentScript.dataset;

function finished(success, count) {
    $.post('/bookle/save-score', {'success':success, 'count':count}, function(data) {
        // 
    });
    window.location.replace(window.location.href+"complete");
}



$(document).ready(function() {
    
    date = data.puzzleDate;

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
        $.get('/bookle/check-guess', {'guess': guess, 'date':date}, function(data) {
            console.log(data);
            const jsonData = JSON.parse(data);

            if (jsonData["valid_guess"]) {
                $("#validGuess").text("");
                count++;
                $("#guessCount").text((maxGuesses-count) + " guesses left");

                if (jsonData["correct_guess"]) {
                    finished(true, count);
                } else {
                    $.get('/bookle/display-guess', {'guess':guess, 'date':date}, function(data) {
                        $("#guessResults").prepend(data);
                    });
                }
            } else {
                $("#validGuess").text("Invalid guess, try again");
            }

            if (count >= maxGuesses) {
                finished(false, count);
            }
        }); 
    });
});