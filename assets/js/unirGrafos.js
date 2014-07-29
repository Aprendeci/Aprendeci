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

    // Conexiones
    jsPlumb.ready(function() {
        // Establecer el contenedor
        jsPlumb.Defaults.Container = "unionGrafos";
        jsPlumb.setContainer("unionGrafos");

        // Crear los puntos de conexion
        $.each($(".conector"), function(idx, obj) {
            jsPlumb.addEndpoint(obj.id, {
                anchor: "AutoDefault",
                connector: "Straight",
                connectorOverlays: [ [ "Arrow", { location:1 } ] ],
                connectorStyle : { lineWidth:5, strokeStyle:"#690F16" },
                endpoint: "Dot",
                isSource: true,
                isTarget: true,
                maxConnections: -1,
                paintStyle: { radius:8, fillStyle:"#690F16" }
            });
        });

        // Hacer las conexiones
        $.each(conceptos, function(idx, obj) {
            var endpointSource = jsPlumb.selectEndpoints({element:'conector' + obj[0]}).get(0);
            var endpointTarget = jsPlumb.selectEndpoints({element:'conector' + obj[1]}).get(0);

            jsPlumb.connect({source:endpointSource, target:endpointTarget});
        });

        // Habilitar el boton de union
        jsPlumb.bind("connection", function(info) {
            habilitarUnion();
        });

        // Eliminacion de enlaces
        jsPlumb.bind("click", function(connection, e) {
            jsPlumb.detach(connection);

            if (jsPlumb.getConnections().length == 0) {
                deshabilitarUnion();
            }
        });

        // Evitar conexiones al mismo grafo
        jsPlumb.bind("beforeDrop", function(info) {
            var sourceGrafo = $("#" + info.sourceId).parent().parent().parent().attr("id");
            var targetGrafo = $("#" + info.targetId).parent().parent().parent().attr("id");

            if (sourceGrafo == targetGrafo) {
                return false;
            } else {
                return true;
            }
        });
    });

    // Unir los grafos
    $(".unir").click(function() {
        if ($(this).hasClass("inactivo")) {
            e.preventDefault();
        } else {
            var nombreGrafo = $("#nombreGrafo").val();

            // Validar nombre del grafo
            if (nombreGrafo == "") {
                $.growl.error({ title:"Error", message: "Debe escribir el nombre del grafo"});
                return false;
            }

            guardar(nombreGrafo);
        }
    });

    // Configurar dialogo de confirmacion
    var dialogo = $("<div></div>")
        .html("<p>No hay conexiones, por lo cual se eliminará el grafo asociado. ¿Desea continuar?</p>")
        .dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            title: "Atención",
            buttons: {
                "Continuar": function() {
                    $(this).dialog("close");
                    guardar("");
                },
                "Cancelar": function() {
                    $(this).dialog("close");
                }
            }
        });

    // Guardar los cambios
    $(".guardar").click(function() {
        // Verificar si no hay conexiones
        if (jsPlumb.getConnections().length == 0) {
            dialogo.dialog("open");
        } else {
            guardar("");
        }
    });

    // Proteccion CSRF
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // Procesar el guardado de informacion
    function guardar(nombreGrafo) {
        var conexiones = jsPlumb.getConnections();
        var dependencias = [];

        // Estructura de las dependencias
        $.each(conexiones, function(index, value) {
            var sourceId = value.sourceId.substr(8);
            var targetId = value.targetId.substr(8);

            dependencias.push([sourceId, targetId]);
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
        $.post("", { "dependencias[]" : dependencias, "nombreGrafo" : nombreGrafo })
            .done(function (data) {
                $.growl.notice({ title: "Éxito", message: data });
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                $.growl.error({ title:"Error", message: "Ha ocurrido un error, intente nuevamente"});
                console.log("jqXHR : " + jqXHR);
                console.log("textStatus : " + textStatus);
                console.log("errorThrown : " + errorThrown);
            });
    }
});