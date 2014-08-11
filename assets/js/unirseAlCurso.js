$(document).ready(function() {

    $("#formularioCurso").submit(function(event) {
        event.preventDefault();

        $.post($(this).attr("action"), $(this).serialize())
            .done(function (data) {
                $("ul.errorlist").remove();
                $("#id_clave").prop("disabled", true);
                $("input[type='submit']").prop("disabled", true);

                $.growl.notice({ title: "Éxito", message: data });
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                var errores = jqXHR.responseJSON;
                var contenido = "<ul class='errorlist'>";

                /* Error de validacion del campo */
                $.each(errores, function(index, value) {
                    contenido += "<li>";
                    contenido += value;
                    contenido += "<li>";
                });
                contenido += "</ul>";
                $("ul.errorlist").remove();
                $("form#formularioCurso").prepend(contenido);

                console.log("jqXHR : " + jqXHR);
                console.log("textStatus : " + textStatus);
                console.log("errorThrown : " + errorThrown);
            });
    });
});