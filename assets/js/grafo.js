$(document).ready(function() {
    var objConceptos = [];

    // Soporte para tooltip
    $("div").tooltip({
        position: {
            my: "bottom",
            at: "bottom+35" }
    });

    // Funcion para obtener un color aleatorio
    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '';

        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.round(Math.random() * 15)];
        }

        return color;
    }

    // Function para agregar un concepto desde un objeto JSON
    function agregarConcepto(objetoJson) {
        var concepto  = $("<div>").attr("id", "concepto" + objetoJson.pk).addClass("concepto");

        // Estilos css
        concepto.css({
            "background-color": "#" + objetoJson.fields.color,
            "background-image": "url(" + objetoJson.fields.imagen + ")",
            "left": objetoJson.fields.x,
            "top": objetoJson.fields.y
        });

        // Titulo para el tooltip
        concepto.attr("title", objetoJson.fields.nombre);

        // Agregar al contenedor de conceptos
        $("#conceptos").append(concepto);

        // Hacer el elemento draggable
        jsPlumb.draggable(concepto, {
            containment: "parent"
        });

        jsPlumb.makeSource(concepto, {
            anchor: [ "Perimeter", { shape:"Circle" } ],
            connector: ["Flowchart", { cornerRadius: "25" } ],
            connectorOverlays: [ [ "Arrow", { location:1 } ] ],
            connectorStyle : { lineWidth:5, strokeStyle:"#" + objetoJson.fields.color },
            deleteEndpointsOnDetach : false,
            paintStyle: { radius:5, fillStyle:"#" + objetoJson.fields.color }
        });

        jsPlumb.makeTarget(concepto, {
            anchor: [ "Perimeter", { shape:"Circle" } ],
            paintStyle: { fillStyle: "#" + objetoJson.fields.color, radius:5 }
        });

        objConceptos.push(concepto);
    }

    // Funcion para agregar un grafo desde un objeto JSON
    function agregarGrafo(objetoJson) {
        var grafo  = $("<div>").attr("id", "grafo" + objetoJson.pk).addClass("concepto");

        // Estilos css
        grafo.css({
            "background-color": "#A22F38",
            "background-image": "url(" + mediaURL + "img/icons/conceptos/defectoGrafo.png)",
            "left": objetoJson.fields.x,
            "top": objetoJson.fields.y
        });

        // Titulo para el tooltip
        grafo.attr("title", objetoJson.fields.nombre);

        // Dirigirse al detalle del grafo al clic
        grafo.dblclick(function() {
            window.location.href = "/aprendeci/grafos/" + objetoJson.pk;
        });

        // Hacer el elemento draggable
        jsPlumb.draggable(grafo, {
            containment: "parent"
        });

        // Agregar al contenedor de conceptos
        $("#conceptos").append(grafo);

        objConceptos.push(grafo);
    }

    // Conexiones
    jsPlumb.ready(function() {
        var zoom = 100;

        // Establecer el contenedor
        jsPlumb.Defaults.Container = "conceptos";
        jsPlumb.setContainer("conceptos");

        // Crear los conceptos
        $.each(conceptos, function(idx, obj) {
            agregarConcepto(obj);
        });

        // Hacer las conexiones de los conceptos
        $.each(conceptos, function(idx, obj) {
            var conexion = {
                overlays: [ [ "Arrow", { location:1 } ] ]
            };

            $.each(obj.fields.requisitos, function (idxr, objr) {
                conexion["source"] = "concepto" + objr.toString();
                conexion["target"] = "concepto" + obj.pk.toString();

                if (document.getElementById(conexion["source"]) != null && document.getElementById(conexion["target"]) != null) {
                    jsPlumb.connect(conexion);
                }
            });
        });

        // Crear los grafos
        $.each(grafos, function(idx, obj) {
            agregarGrafo(obj);
        });

        // Hacer las conexiones de los grafos
        $.each(grafosRel, function(idx, obj) {
            var conexion = {
                anchor: [ "Perimeter", { shape:"Circle" } ],
                connector: ["Flowchart", { cornerRadius: "25" } ],
                endpointStyle : { radius:5, strokeStyle:"#A22F38" },
                overlays: [ [ "Arrow", { location:1 } ] ],
                paintStyle: { lineWidth:5, strokeStyle:"#A22F38" }
            };

            conexion["source"] = "grafo" + obj[0];
            conexion["target"] = "grafo" + obj[1];

            if (document.getElementById(conexion["source"]) != null && document.getElementById(conexion["target"]) != null) {
                jsPlumb.connect(conexion);
            }
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

    // Dialogo para crear concepto
    $("#conceptoDialog").dialog({
        autoOpen: false,
        modal: true,
        resizable: false,
        width: 400
    });

    // Dialogo para agregar grafo
    $("#grafoDialog").dialog({
        autoOpen: false,
        modal: true,
        resizable: false,
        width: 400
    });

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
            var sourceId = value.sourceId;
            var targetId = value.targetId;

            dependencias.push([sourceId, targetId]);
        });

        // Estructura de las posiciones
        $.each(objConceptos, function(index, value) {
            var posicion = {
                nodo: value.attr("id"),
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

    // Agregar concepto directamente
    var posX, posY;

    $("#conceptos").mousedown(function(e) {
        if (e.which == 3) {
            posX = Math.round(e.pageX - $(this).offset().left);
            posY = Math.round(e.pageY - $(this).offset().top);
        }
    });

    $.contextMenu({
        selector: '#conceptos',
        items: {
            "concepto": {
                name: "Concepto",
                icon:"concepto",
                callback: function(key, options) {
                    // Completar los datos del concepto
                    $("#id_color").val(getRandomColor());
                    $("#id_x").val(posX);
                    $("#id_y").val(posY);
                    $("#id_grafo").val(grafoId);

                    // Mostrar dialogo
                    $("#conceptoDialog").dialog("open");
                }
            },
            "grafo": {
                name: "Grafo",
                icon:"grafo",
                callback: function(key, options) {
                    // Mostrar dialogo
                    $("#grafoDialog").dialog("open");
                }
            }
        }
    });

    // Guardar el concepto
    $("#formularioConcepto").submit(function(event) {
        event.preventDefault();

        $.post($(this).attr("action"), $(this).serialize())
            .done(function (data) {
                $("p.error").remove();
                $("input[type='submit']").prop("disabled", true);

                // Cerrar el dialogo
                $("#conceptoDialog").dialog("close");

                // Agregar concepto al canvas
                data[0].fields.imagen = mediaURL + data[0].fields.imagen;
                agregarConcepto(data[0]);
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                var contenido = "<p class='error'>Error al agregar el concepto</p>";

                $("p.error").remove();
                $("form#formularioConcepto").prepend(contenido);

                console.log("jqXHR : " + jqXHR);
                console.log("textStatus : " + textStatus);
                console.log("errorThrown : " + errorThrown);
            });
    });

    // Mostrar informacion del concepto
    $(".concepto").click(function() {
        var id = $(this).attr("id").substring(8);
        var concepto = null;

        for (var i = 0; i < conceptos.length; i++) {
            if (conceptos[i].pk == id) {
                concepto = conceptos[i];
            }
        }

        if (concepto != null) {
            var url = "/aprendeci/concepto/" + concepto.pk + "/";
            var contenido = "<p>" + concepto.fields.descripcion + "</p><br />";
            contenido += "<a href='" + url + "' class='button small ver'>Ver más</a>";

            $("<div></div>").attr("title", concepto.fields.nombre).html(contenido).dialog({
                resizable: false,
                width: 250
            });
        }
    });
});