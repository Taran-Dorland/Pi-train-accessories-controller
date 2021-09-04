$(document).ready(function () {

    $.getJSON("http://192.168.0.230:12080/json/turnouts", function (data) {

        console.log(data);
    });

});