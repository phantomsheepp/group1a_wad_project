// from django docs
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var maxGuesses = 3;
let count = 0;
var data = document.currentScript.dataset;

function finished(success, count, date) {
    var user = data.user;
    var dataInput = {'success':success, 'count':count, 'date':date, 'user':user}

    $.ajax({
        url: '/bookle/save-score/',
        method : 'POST',
        data : JSON.stringify(dataInput),
        headers: {'X-CSRFToken': csrftoken},
        success: function(data) {}
    });

    //$.get('/bookle/puzzle/.../complete');
}


$(document).ready(function() {
    
    date = data.puzzleDate;

    $("#guessCount").text(maxGuesses + " guesses left");

    // Show book suggestions as the user types a guess
    $("#guessInput").keyup(function() {
        var guess = $(this).val();

        $.get('/bookle/suggestions', {'guess': guess}, function(data) {
            $("#options").html(data);
        });
    });

    
    $("#submitButton").click(function() {
        var guess = $("#guessInput").val();
        let dataInput = {'guess': guess, 'date':date}

        // Check and validate user guess input
        $.get('/bookle/check-guess', dataInput, function(data) {
            console.log(data);
            const jsonData = JSON.parse(data);

            if (jsonData["valid_guess"]) {
                $("#validGuess").text("");
                count++;
                $("#guessCount").text((maxGuesses-count) + " guesses left");

                // Finish puzzle if correct guess, else display guess information
                if (jsonData["correct_guess"]) {
                    finished(true, count, date);
                } else {
                    $.get('/bookle/display-guess', {'guess':guess, 'date':date}, function(data) {
                        $("#guessResults").prepend(data);
                    });
                }
            } else {
                $("#validGuess").text("Invalid guess, try again");
            }

            // Finish puzzle if out of guesses 
            if (count >= maxGuesses) {
                finished(false, count, date);
            }
        }); 
    });
});

