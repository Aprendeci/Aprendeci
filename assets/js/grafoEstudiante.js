$(document).ready(function() {
    var objConceptos = [];

    // Conexiones
    jsPlumb.ready(function() {
        // Establecer el contenedor
        jsPlumb.Defaults.Container = "conceptos";
        jsPlumb.setContainer("conceptos");

        // Crear los conceptos
        $.each(conceptos, function(idx, obj) {
            var concepto  = $("<div>").attr("id", "concepto" + obj.pk).addClass("concepto");
            var drag = $("<div>").addClass("drag");

            concepto.css({
                "background-image": "url(" + obj.fields.imagen + ")",
                "cursor": "pointer",
                "left": obj.fields.x,
                "top": obj.fields.y
            });

            concepto.click(function() {
                location.href = "http://" + location.host + "/aprendeci/estudiante/concepto/" + obj.pk;
            });

            concepto.append(drag);
            $("#conceptos").append(concepto);

            objConceptos.push(concepto);
        });

        // Hacer las conexiones
        $.each(conceptos, function(idx, obj) {
            var conexion = {
                anchor: [ "Perimeter", { shape:"Circle" } ],
                connector: ["Flowchart", { cornerRadius: "25" } ],
                endpointStyle: { fillStyle: "#690F16", radius:5 },
                paintStyle : { lineWidth:5, strokeStyle:"#690F16" },
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
    });
});