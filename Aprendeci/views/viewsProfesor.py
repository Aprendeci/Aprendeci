from django.core import serializers
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from Aprendeci.models import *
from .viewsGeneral import *
import json


# Class based views

# Vista principal
class PerfilProfesorView(LoginRequiredMixin, TemplateView):
    template_name = 'Aprendeci/profesor/perfil.html'


class CursosProfesorView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = "Aprendeci/profesor/cursos.html"

    def get_queryset(self):
        return self.model.objects.filter(profesor=self.request.user)


# Vista de la lista de grafos
class GrafosView(LoginRequiredMixin, ListView):
    model = Grafo
    template_name = "Aprendeci/profesor/grafo/grafos.html"


# Vista del grafo
class GrafoView(LoginRequiredMixin, ListView):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "Aprendeci/profesor/grafo/grafo.html"

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
class ConceptosGrafoView(LoginRequiredMixin, ListView):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "Aprendeci/profesor/grafo/conceptos.html"

    def get_context_data(self, **kwargs):
        context = super(ConceptosGrafoView, self).get_context_data(**kwargs)
        context['grafo_id'] = self.kwargs['id']
        context['grafo_nombre'] = Grafo.objects.get(pk=self.kwargs['id']).nombre
        return context

    def get_queryset(self):
        grafo_id = self.kwargs['id']
        return Concepto.objects.filter(grafo=grafo_id)


# Vista en detalle de un concepto
class ConceptoView(LoginRequiredMixin, DetailView):
    context_object_name = "concepto"
    model = Concepto
    template_name = "Aprendeci/profesor/grafo/concepto.html"

    def get_context_data(self, **kwargs):
        context = super(ConceptoView, self).get_context_data(**kwargs)
        context['grafo_id'] = Concepto.objects.get(pk=self.kwargs['pk']).grafo.id
        return context


class UnirGrafosView(LoginRequiredMixin, ListView):
    conexiones = []
    context_object_name = "grafo_list"
    model = Grafo
    template_name = "Aprendeci/profesor/grafo/unirGrafos.html"

    def dispatch(self, request, *args, **kwargs):
        # Obtener relaciones entre grafos
        self.conexiones = []
        for concepto in Concepto.objects.filter(Q(grafo=self.request.GET.get("grafo1")) | Q(grafo=self.request.GET.get("grafo2"))):
            for requisito in concepto.requisitos.all():
                if requisito.grafo_id != concepto.grafo_id:
                    self.conexiones.append([requisito.id, concepto.id])

        return super(UnirGrafosView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UnirGrafosView, self).get_context_data(**kwargs)
        try:
            grafo1 = Grafo.objects.get(pk=self.request.GET.get("grafo1"))
            grafo2 = Grafo.objects.get(pk=self.request.GET.get("grafo2"))

            if not grafo1.grafoPadre is None and not grafo2.grafoPadre is None and grafo1.grafoPadre == grafo2.grafoPadre:
                context['conexiones'] = json.dumps(self.conexiones)
                context['modificacion'] = True
            else:
                context['conexiones'] = json.dumps([])
                context['modificacion'] = False
        except:
            context['modificacion'] = False
        return context

    def get_queryset(self):
        try:
            grafo1 = Grafo.objects.get(pk=self.request.GET.get("grafo1"))
            grafo2 = Grafo.objects.get(pk=self.request.GET.get("grafo2"))
            lista = {grafo1, grafo2}
        except:
            lista = {}
        return lista

    def post(self, request, *args, **kwargs):
        dependencias = request.POST.getlist("dependencias[]")
        nombreGrafo = request.POST.get("nombreGrafo")

        # Obtener relaciones entre grafos y limpiarlas
        for conexion in self.conexiones:
            preRequisito = Concepto.objects.get(pk=conexion[0])
            concepto = Concepto.objects.get(pk=conexion[1])

            concepto.requisitos.remove(preRequisito)

        # Crear dependencias
        for dependencia in dependencias:
            tupla = dependencia.partition(",")
            preRequisito = Concepto.objects.get(pk=tupla[0])
            concepto = Concepto.objects.get(pk=tupla[2])

            concepto.requisitos.add(preRequisito)

        # Manipular el grafo padre
        grafo1 = Grafo.objects.get(pk=self.request.GET.get("grafo1"))
        grafo2 = Grafo.objects.get(pk=self.request.GET.get("grafo2"))
        if len(dependencias) > 0:
            # Crear nuevo grafo si no existe
            if grafo1.grafoPadre is None:
                nuevoGrafo = Grafo(nombre=nombreGrafo)
                nuevoGrafo.save()

                grafo1.grafoPadre = nuevoGrafo
                grafo2.grafoPadre = nuevoGrafo

                grafo1.save()
                grafo2.save()
        else:
            # Eliminar el grafo padre
            grafoPadre = grafo1.grafoPadre

            grafo1.grafoPadre = None
            grafo2.grafoPadre = None

            grafo1.save()
            grafo2.save()

            grafoPadre.delete()

        return HttpResponse("Se ha guardado exitosamente")