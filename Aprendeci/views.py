from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files import File
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from Aprendeci.models import *
import json
import logging

'''
Configuracion general
'''
logger = logging.getLogger('aprendeci')

'''
Mixins
'''

# Mixin para la autenticacion
class LoginRequiredMixin(object):
    @classmethod
    def as_view(self, **kwargs):
        view = super(LoginRequiredMixin, self).as_view(**kwargs)
        return login_required(view)

'''
Class based views
'''

# Vista de la lista de grafos
class GrafosView(ListView, LoginRequiredMixin):
    model = Grafo
    template_name = "Aprendeci/grafo/lista.html"

# Vista del grafo
class GrafoView(ListView, LoginRequiredMixin):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "Aprendeci/grafo/grafo.html"

    def get_queryset(self):
        grafo_id = self.kwargs['id']
        return serializers.serialize("json", self.model.objects.filter(grafo=grafo_id))

    def post(self, request, *args, **kwargs):
        dependencias = request.POST.getlist("dependencias[]")
        posiciones = request.POST.getlist("posiciones[]")

        # Limpiar dependencias
        grafo_id = self.kwargs['id']
        for concepto in self.model.objects.filter(grafo=grafo_id):
            concepto.requisitos.clear()

        # Crear dependencias
        for dependencia in dependencias:
            tupla = dependencia.partition(",")
            preRequisito = self.model.objects.get(pk=tupla[0])
            concepto = self.model.objects.get(pk=tupla[2])

            concepto.requisitos.add(preRequisito)

        # Actualizar posiciones
        for posicion in posiciones:
            posicionDict = json.loads(posicion)
            concepto = self.model.objects.get(pk=posicionDict['concepto'])
            concepto.x = round(posicionDict['x'])
            concepto.y = round(posicionDict['y'])

            concepto.save()

        # Guardar el grafo
        grafoMat = "{{" + "},{".join(dependencias) + "}}"
        with open('uploads/txt/grafo.txt', 'w+') as f:
            file = File(f)
            file.write(grafoMat)

        return HttpResponse("Se ha guardado exitosamente")

# Vista de la lista de conceptos de un grafo
class ConceptosGrafoView(ListView, LoginRequiredMixin):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "Aprendeci/grafo/conceptos.html"

    def get_context_data(self, **kwargs):
        context = super(ConceptosGrafoView, self).get_context_data(**kwargs)
        context['grafo_id'] = self.kwargs['id']
        context['grafo_nombre'] = Grafo.objects.get(pk=self.kwargs['id']).nombre
        return context

    def get_queryset(self):
        grafo_id = self.kwargs['id']
        return Concepto.objects.filter(grafo=grafo_id)

# Vista en detalle de un concepto
class ConceptoView(DetailView):
    context_object_name = "concepto"
    model = Concepto
    template_name = "Aprendeci/grafo/concepto.html"

    def get_context_data(self, **kwargs):
        context = super(ConceptoView, self).get_context_data(**kwargs)
        context['grafo_id'] = Concepto.objects.get(pk=self.kwargs['pk']).grafo.id
        return context