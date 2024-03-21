var data = document.currentScript.dataset;

$(document).ready(function() {
   

    date = window.location.pathname.split('/')[3];
    console.log(date);
    
    var dataInput = {'date':date};

    $.get('/bookle/get-book-data', dataInput, function(data) {
        console.log(data);
        const jsonData = JSON.parse(data);
        var guesses = jsonData['guesses'];

        if (jsonData['success']) {
            $(".final-guess-count").text("It took you "+guesses+" guesses");
        }

        $("#cover").attr('src', jsonData['cover']);
        $("#title").text(jsonData['title']);
        $("#author").text(jsonData['author']);
        $("#releaseYear").text(jsonData['release_year']);
        

        if (date != "daily") {
            $('.discussion-link').hide();
        }
    });

});