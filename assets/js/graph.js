jsPlumb.ready(function() {

    var contenedor = $('#canvas');
    var h = contenedor.height();

    // Establecer el contenedor
    jsPlumb.setContainer('canvas');

    // Crear los conceptos
    $.each(conceptos, function(idx, obj) {
        var concepto  = $('<div>').attr('id', 'concepto' + obj.pk).addClass('concepto');
        var drag = $('<div>').addClass('drag');

        concepto.css({
            'background-image': 'url(' + obj.fields.imagen + ')',
            'left': obj.fields.x,
            'top': obj.fields.y
        });

        concepto.append(drag);
        $('#canvas').append(concepto);

        jsPlumb.draggable(concepto, {
            containment: 'parent'
        });

        jsPlumb.makeSource(drag, {
            anchor:[ "Perimeter", { shape:"Circle" } ],
            connector: ['Bezier', { curviness: '25' } ],
            connectorOverlays: [ [ "Arrow", { location:1 } ] ],
            connectorStyle : { lineWidth:5, strokeStyle:'#690F16' },
            deleteEndpointsOnDetach : false,
            paintStyle:{ radius:5, fillStyle:'#690F16' },
            parent: concepto
        });

        jsPlumb.makeTarget(concepto, {
            anchor:[ "Perimeter", { shape:"Circle" } ],
            paintStyle: { fillStyle: '#690F16', radius:5 }
        });
    });

    // Hacer las conexiones
    $.each(conceptos, function(idx, obj) {
        var conexion = {
            overlays: [ [ "Arrow", { location:1 } ] ]
        };

        $.each(obj.fields.requisitos, function (idxr, objr) {
            conexion["source"] = 'concepto' + objr.toString();
            conexion["target"] = 'concepto' + obj.pk.toString();

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

});