$(document).ready(function() {
    // Proteccion CSRF
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // Guardar grafo
    $(".guardar").click(function() {
        var calificaciones = new Object();

        // Obtener valor de las calificaciones
        $("input[type='number']").each(function() {
            calificaciones[$(this).attr("name")] = $(this).val();
        });

        // Seguridad de CSRF
        var csrftoken = $.cookie('csrftoken');
        $.ajaxSetup({
            crossDomain: false,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        // Envio al backend de los datos
        $.post("", { "calificaciones" : JSON.stringify(calificaciones) })
        .done(function (data) {
            $.growl.notice({ title: "Éxito", message: data });
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
                $.growl.error({ title:"Error", message: "No se han podido guardar las calificaciones"});
                console.log("jqXHR : " + jqXHR);
                console.log("textStatus : " + textStatus);
                console.log("errorThrown : " + errorThrown);
        });
    });
});