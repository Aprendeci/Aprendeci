from django import forms
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.generic import DetailView, ListView, TemplateView, FormView
from Aprendeci.models import Concepto, Curso, Calificaciones
from .viewsGeneral import *
import json


# Class based views

# Vista principal
class PerfilEstudianteView(LoginRequiredMixin, EstudianteRequiredMixin, ListView):
    model = Curso
    template_name = 'Aprendeci/estudiante/perfil.html'

    def get_queryset(self):
        return self.model.objects.filter(estudiantes__pk=self.request.user.estudiante.pk)


# Vista con el listado de cursos
class CursosEstudianteView(LoginRequiredMixin, EstudianteRequiredMixin, ListView):
    model = Curso
    template_name = "Aprendeci/estudiante/cursos.html"

    def get_queryset(self):
        return Curso.objects.exclude(estudiantes__id__exact=self.request.user.estudiante.id)


# Vista para unirse a un curso
class UnirseAlCursoForm(forms.Form):
    clave = forms.CharField(label='Clave', max_length='100')

    def unirEstudiante(self, curso_id, estudiante):
        curso = Curso.objects.get(pk=curso_id)
        if self.cleaned_data['clave'] == curso.clave:
            estudiante.enrolarse(curso)
            return True
        return False


class UnirseAlCursoEstudianteView(LoginRequiredMixin, EstudianteRequiredMixin, FormView):
    form_class = UnirseAlCursoForm
    template_name = "Aprendeci/estudiante/unirseAlCurso.html"

    def get_context_data(self, **kwargs):
        context = super(UnirseAlCursoEstudianteView, self).get_context_data(**kwargs)
        context['curso'] = Curso.objects.get(pk=self.kwargs['id'])
        return context

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return super(UnirseAlCursoEstudianteView, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            if not form.unirEstudiante(self.kwargs['id'], self.request.user.estudiante):
                return JsonResponse({'error': 'La clave es incorrecta'}, status=400)
            else:
                return HttpResponse("Se ha inscrito correctamente al curso")
        else:
            return super(UnirseAlCursoEstudianteView, self).form_valid(form)


# Vista de un curso del estudiante
class CursoEstudianteView(LoginRequiredMixin, EstudianteRequiredMixin, TemplateView):
    template_name = "Aprendeci/estudiante/curso.html"

    def get_context_data(self, **kwargs):
        context = super(CursoEstudianteView, self).get_context_data(**kwargs)

        curso = Curso.objects.get(pk=self.kwargs['id'])

        conceptos = curso.grafo.obtener_conceptos(True)
        estados = list()

        for c in conceptos:
            calificacion = Calificaciones.objects.filter(estudiante__usuario=self.request.user).filter(concepto=c)
            if calificacion[0].calificacion >= c.porcentajeBase:
                estados.append(True)
            else:
                estados.append(False)

        context['curso_nombre'] = curso.nombre
        context['concepto_list'] = serializers.serialize("json", conceptos)
        context['estado_list'] = json.dumps(estados)

        return context


# Vista en detalle de un concepto
class ConceptoEstudianteView(LoginRequiredMixin, EstudianteRequiredMixin, DetailView):
    context_object_name = "concepto"
    model = Concepto
    template_name = "Aprendeci/estudiante/concepto.html"

    def get_context_data(self, **kwargs):
        context = super(ConceptoEstudianteView, self).get_context_data(**kwargs)
        context['grafo_id'] = Concepto.objects.get(pk=self.kwargs['pk']).grafo.id
        return context