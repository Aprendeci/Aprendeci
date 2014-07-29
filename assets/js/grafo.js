$(document).ready(function() {
    var objConceptos = [];

    // Conexiones
    jsPlumb.ready(function() {
        var zoom = 100;

        // Establecer el contenedor
        jsPlumb.Defaults.Container = "conceptos";
        jsPlumb.setContainer("conceptos");

        // Crear los conceptos
        $.each(conceptos, function(idx, obj) {
            var concepto  = $("<div>").attr("id", "concepto" + obj.pk).addClass("concepto");
            var drag = $("<div>").addClass("drag");

            concepto.css({
                "background-image": "url(" + obj.fields.imagen + ")",
                "left": obj.fields.x,
                "top": obj.fields.y
            });

            concepto.append(drag);
            $("#conceptos").append(concepto);

            // Hacer el elemento draggable
            jsPlumb.draggable(concepto, {
                containment: "parent"
            });

            jsPlumb.makeSource(concepto, {
                anchor: [ "Perimeter", { shape:"Circle" } ],
                connector: ["Flowchart", { cornerRadius: "25" } ],
                connectorOverlays: [ [ "Arrow", { location:1 } ] ],
                connectorStyle : { lineWidth:5, strokeStyle:"#690F16" },
                deleteEndpointsOnDetach : false,
                paintStyle: { radius:5, fillStyle:"#690F16" }
            });

            jsPlumb.makeTarget(concepto, {
                anchor: [ "Perimeter", { shape:"Circle" } ],
                paintStyle: { fillStyle: "#690F16", radius:5 }
            });

            objConceptos.push(concepto);
        });

        // Hacer las conexiones
        $.each(conceptos, function(idx, obj) {
            var conexion = {
                overlays: [ [ "Arrow", { location:1 } ] ]
            };

            $.each(obj.fields.requisitos, function (idxr, objr) {
                conexion["source"] = "concepto" + objr.toString();
                conexion["target"] = "concepto" + obj.pk.toString();

                jsPlumb.connect(conexion);
            });
        });

        // Eliminacion de enlaces
        jsPlumb.bind("click", function(connection, e) {
            jsPlumb.detach(connection);
        });

        // Evitar auto-conexiones
        jsPlumb.bind("beforeDrop", function(info) {
            var s = info.sourceId, c = info.targetId;

            if (s == c) {
                return false;
            } else {
                return true;
            }
        });

        // Zoom
        $(".zoomIn").click(function() {
            if (zoom < 100) {
                zoom += 10;
                setZoom(zoom, jsPlumb);
            }
        });

        $(".zoomOut").click(function() {
            if (zoom > 10) {
                zoom -= 10;
                setZoom(zoom, jsPlumb);
            }
        });

        // Deshabilita incialmente el modo de union
        $.each(objConceptos, function(index, value) {
            jsPlumb.setTargetEnabled(value);
            jsPlumb.setSourceEnabled(value);
        });
    });

    // Cambio de modo
    $("input:radio").change(function() {
        var modo = this;

        $.each(objConceptos, function(index, value) {
            // Cambia el modo de arrastre
            jsPlumb.toggleDraggable(value);

            // Cambia el puntero y el modo de union
            if (modo.id == "mover") {
                value.css("cursor", "move");
                jsPlumb.setTargetEnabled(value, false).setSourceEnabled(value, false);
            } else if (modo.id == "unir") {
                value.css("cursor", "pointer");
                jsPlumb.setTargetEnabled(value, true).setSourceEnabled(value, true);
            }
        });
    });

    // Cambiar zoom
    function setZoom(zoom, instance) {
        var transformOrigin = [ 0.5, 0.5 ],
            el = document.getElementById(instance.Defaults.Container),
            p = [ "webkit", "moz", "ms", "o" ],
            s = "scale(" + (zoom / 100) + ")",
            oString = (transformOrigin[0] * 100) + "% " + (transformOrigin[1] * 100) + "%";

        for (var i = 0; i < p.length; i++) {
            el.style[p[i] + "Transform"] = s;
            el.style[p[i] + "TransformOrigin"] = oString;
        }

        el.style["transform"] = s;
        el.style["transformOrigin"] = oString;

        instance.setZoom(zoom / 100);

        $(".zoom span").text(zoom + "%");
    };

    // Proteccion CSRF
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // Guardar grafo
    $(".guardar").click(function() {
        var conexiones = jsPlumb.getConnections();
        var dependencias = [];
        var posiciones = [];

        // Estructura de las dependencias
        $.each(conexiones, function(index, value) {
            var sourceId = value.sourceId.substr(8);
            var targetId = value.targetId.substr(8);

            dependencias.push([sourceId, targetId]);
        });

        // Estructura de las posiciones
        $.each(objConceptos, function(index, value) {
            var posicion = {
                concepto: value.attr("id").substr(8),
                x: value.position().left,
                y: value.position().top
            };

            posiciones.push(JSON.stringify(posicion));
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
        $.post("", { "dependencias[]" : dependencias, "posiciones[]" : posiciones })
        .done(function (data) {
            $.growl.notice({ title: "Éxito", message: data });
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
                $.growl.error({ title:"Error", message: "No se ha podido guardar el grafo"});
                console.log("jqXHR : " + jqXHR);
                console.log("textStatus : " + textStatus);
                console.log("errorThrown : " + errorThrown);
        });
    });
});