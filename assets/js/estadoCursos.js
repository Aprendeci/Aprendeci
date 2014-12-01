$(document).ready(function() {

    var options = {
        scaleGridLineColor : "rgba(255,255,255,.05)",
        scaleLineColor: "rgba(255,255,255,.1)",
        scaleFontColor: "#FFF"
    };

    $.each(cursos, function(index, value) {
        var ctx = $("#chart" + value.curso).get(0).getContext("2d");
        var chart = new Chart(ctx);

        var data = {
            labels: value.conceptos,
            datasets: [
                {
                    label: "My First dataset",
                    fillColor: "rgba(220,220,220,0.5)",
                    strokeColor: "rgba(220,220,220,0.8)",
                    highlightFill: "rgba(220,220,220,0.75)",
                    highlightStroke: "rgba(220,220,220,1)",
                    data: value.aprobados
                }
            ]
        }

        chart.Bar(data, options);
    });

});