/*var button = document.getElementById("submit-button");
button.addEventListener("click", showOptions);

function showOptions() {
    print("hi");
    document.getElementById("guess-title").style.BackgroundColor = "green";
}
*/


// JQuery
/*$("#submit-button").on("click", function() {
    $("#submit-button").text("hello");
});

$(document).ready(function() {
    $("#submit-button").text("hello");
})*/

$(document).ready(function() {
    alert("HELLO");

    $("#submit-button").click(function() {
        alert("button");
        $("#guess-label").css("color","blue");
      });
});

