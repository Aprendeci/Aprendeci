from django import forms
from django.core import serializers
from django.core.files import File
from django.db.models import Q
from django.forms import HiddenInput
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from Aprendeci.models import *
from .viewsGeneral import *
import json


# Class based views

# Vista principal
class PerfilProfesorView(LoginRequiredMixin, TemplateView):
    template_name = 'Aprendeci/profesor/perfil.html'


# Vista de los cursos
class CursosProfesorView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = "Aprendeci/profesor/cursos.html"

    def get_queryset(self):
        return self.model.objects.filter(profesor=self.request.user.profesor)


# Vista de los estudiantes de un curso
class EstudiantesView(LoginRequiredMixin, ListView):
    model = Estudiante
    template_name = "Aprendeci/profesor/estudiantes.html"

    def get_context_data(self, **kwargs):
        context = super(EstudiantesView, self).get_context_data(**kwargs)
        context['curso_nombre'] = Curso.objects.get(pk=self.kwargs['id']).nombre
        context['curso_id'] = self.kwargs['id']
        return context

    def get_queryset(self):
        return self.model.objects.filter(estudiantes__id=self.kwargs['id'])


# Vista de los conceptos de un estudiante
class EstudianteView(LoginRequiredMixin, ListView):
    context_object_name = "calificaciones_set"
    model = Calificaciones
    template_name = "Aprendeci/profesor/estudiante.html"

    def get_context_data(self, **kwargs):
        context = super(EstudianteView, self).get_context_data(**kwargs)
        context['curso'] = Curso.objects.get(pk=self.kwargs['cursoId'])
        context['estudiante'] = Estudiante.objects.get(pk=self.kwargs['estudianteId'])
        return context

    def get_queryset(self):
        calificaciones = list()
        calEstudiante = self.model.objects.filter(estudiante__pk=self.kwargs['estudianteId'])
        for cal in calEstudiante.all():
            if (cal.concepto.pertenece_al_curso(self.kwargs['cursoId'])):
                calificaciones.append(cal)
        return calificaciones

    def post(self, request, *args, **kwargs):
        calificaciones = json.loads(request.POST.get("calificaciones"))

        for key, value in calificaciones.items():
            calificacion = Calificaciones.objects.get(pk=key[12:])
            calificacion.calificacion = value
            calificacion.save()

        return HttpResponse("Se ha guardado exitosamente")


# Vista de la lista de grafos
class GrafosView(LoginRequiredMixin, ListView):
    model = Grafo
    template_name = "Aprendeci/profesor/grafo/grafos.html"


# Formulario del concepto
class ConceptoForm(ModelForm):
    class Meta:
        model = Concepto
        exclude = ['requisitos', 'fecha_creacion', 'porcentajeBase']
        widgets = {
            'color': HiddenInput(),
            'grafo': HiddenInput(),
            'x': HiddenInput(),
            'y': HiddenInput()
        }


# Funcion para agregar un concepto via AJAX
def agregar_concepto(request):
    if request.is_ajax() and request.method == "POST":
        form = ConceptoForm(request.POST)
        if form.is_valid():
            concepto = form.save()
            return HttpResponse(serializers.serialize("json", Concepto.objects.filter(pk=concepto.pk)), content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)


class GrafoForm(forms.Form):
    grafosPosibles = forms.ChoiceField(widget=forms.Select, choices=(('1', 'First',), ('2', 'Second',)))


# Vista del grafo
class GrafoView(LoginRequiredMixin, ListView):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "Aprendeci/profesor/grafo/grafo.html"

    def get_context_data(self, **kwargs):
        context = super(GrafoView, self).get_context_data(**kwargs)

        grafos = Grafo.objects.get(pk=self.kwargs['id']).obtener_grafos()
        grafosPosibles = Grafo.objects.get(pk=self.kwargs['id']).obtener_grafos_posibles()

        # Obtener relaciones de los grafos
        relacionesGrafo = []
        for grafo in grafos:
            for grafoAux in grafos:
                if grafo != grafoAux:
                    if grafo.esta_relacionado_con(grafoAux.pk):
                        relacionesGrafo.append([grafo.pk, grafoAux.pk])

        # Variables del contexto
        context['concepto_form'] = ConceptoForm()
        context['grafo_form'] = GrafoForm()
        context['grafo_id'] = self.kwargs['id']
        context['grafo_nombre'] = Grafo.objects.get(pk=self.kwargs['id']).nombre
        context['grafos_list'] = serializers.serialize("json", grafos)
        context['grafos_rel'] = json.dumps(relacionesGrafo)
        context['grafos_posibles'] = serializers.serialize("json", grafosPosibles)

        return context

    def get_queryset(self):
        grafo_id = self.kwargs['id']
        return serializers.serialize("json", Grafo.objects.get(pk=grafo_id).obtener_conceptos(False))

    def post(self, request, *args, **kwargs):
        dependencias = request.POST.getlist("dependencias[]")
        posiciones = request.POST.getlist("posiciones[]")

        # Limpiar dependencias
        grafo_id = self.kwargs['id']
        for concepto in Grafo.objects.get(pk=grafo_id).obtener_conceptos(False):
            concepto.requisitos.clear()

        # Crear dependencias
        for dependencia in dependencias:
            tupla = dependencia.partition(",")

            if tupla[0].startswith("concepto"):
                preRequisito = self.model.objects.get(pk=tupla[0][8:])
                concepto = self.model.objects.get(pk=tupla[2][8:])

                concepto.requisitos.add(preRequisito)

        # Actualizar posiciones
        for posicion in posiciones:
            posicionDict = json.loads(posicion)

            if posicionDict["nodo"].startswith("concepto"):
                concepto = self.model.objects.get(pk=posicionDict['nodo'][8:])
                concepto.x = round(posicionDict['x'])
                concepto.y = round(posicionDict['y'])

                concepto.save()
            elif posicionDict["nodo"].startswith("grafo"):
                grafo = Grafo.objects.get(pk=posicionDict['nodo'][5:])
                grafo.x = round(posicionDict['x'])
                grafo.y = round(posicionDict['y'])

                grafo.save()

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