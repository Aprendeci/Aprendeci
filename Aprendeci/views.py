from _ast import List
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files import File
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from Aprendeci.models import *

class JSONResponseMixin(object):
    def get_queryset(self):
        return serializers.serialize("json", self.model.objects.all())

class IndexView(JSONResponseMixin, ListView):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "aprendeci/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        dependencias = request.POST.getlist("dependencias[]")

        # Limpiar dependencias
        for concepto in self.model.objects.all():
            concepto.requisitos.clear()

        # Crear dependencias
        for dependencia in dependencias:
            tupla = dependencia.partition(",")
            preRequisito = self.model.objects.get(pk=tupla[0])
            concepto = self.model.objects.get(pk=tupla[2])

            concepto.requisitos.add(preRequisito)

        # Guardar el grafo
        grafoMat = "{{" + "},{".join(dependencias) + "}}"
        with open('uploads/txt/grafo.txt', 'w+') as f:
            file = File(f)
            file.write(grafoMat)

        return HttpResponse("Se ha guardado exitosamente")

class GrafoView(ListView):
    model = Grafo
    template_name = "aprendeci/grafo/lista.html"