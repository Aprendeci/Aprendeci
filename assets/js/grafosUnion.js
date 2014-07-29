$(document).ready(function() {
    // Habilita el enlace de union
    function habilitarUnion() {
        $(".unir").removeClass("inactivo");
    }

    // Deshabilita el enlace de union
    function deshabilitarUnion() {
        $(".unir").addClass("inactivo");
    }

    deshabilitarUnion();

    // Evento de seleccion
    $("input[type='checkbox']").on("click", function() {
        if ($("input:checkbox:checked").length == 2) {
            habilitarUnion();
        } else {
            deshabilitarUnion();
        }
    });

    // Bloquear enlace si esta inactivo
    $(".unir").click(function(e) {
        if ($(this).hasClass("inactivo")) {
            e.preventDefault();
        } else {
            e.preventDefault();
            location.href= $(this).attr("href") + "?grafo1=" + $("input:checkbox:checked")[0].value + "&grafo2=" + $("input:checkbox:checked")[1].value;
        }
    });
});