$(document).ready(function() {

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

            jsPlumb.draggable(concepto, {
                containment: "parent"
            });

            jsPlumb.makeSource(drag, {
                anchor:[ "Perimeter", { shape:"Circle" } ],
                connector: ["Bezier", { curviness: "25" } ],
                connectorOverlays: [ [ "Arrow", { location:1 } ] ],
                connectorStyle : { lineWidth:5, strokeStyle:"#690F16" },
                deleteEndpointsOnDetach : false,
                paintStyle:{ radius:5, fillStyle:"#690F16" },
                parent: concepto
            });

            jsPlumb.makeTarget(concepto, {
                anchor:[ "Perimeter", { shape:"Circle" } ],
                paintStyle: { fillStyle: "#690F16", radius:5 }
            });
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

    // Guardar grafo
    $(".guardarGrafo").click(function() {
        var dependencias = jsPlumb.getConnections();
    });
});