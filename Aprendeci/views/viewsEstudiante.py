from django import forms
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView, FormView
from Aprendeci.models import Concepto, Curso
from .viewsGeneral import *


# Class based views

# Vista principal
class PerfilEstudianteView(LoginRequiredMixin, TemplateView):
    template_name = 'Aprendeci/estudiante/perfil.html'


# Vista con el listado de cursos
class CursosEstudianteView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = "Aprendeci/estudiante/cursos.html"


# Vista para unirse a un curso
class UnirseAlCursoForm(forms.Form):
    clave = forms.CharField(label='Clave', max_length='100')

    def unirEstudiante(self, curso_id, estudiante):
        curso = Curso.objects.get(pk=curso_id)
        if self.cleaned_data['clave'] == curso.clave:
            estudiante.enrolarse(curso)
            return True
        return False


class UnirseAlCursoEstudianteView(LoginRequiredMixin, FormView):
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
                return JsonResponse({'error': 'La clave es incorrecta' }, status=400)
            else:
                return HttpResponse("Se ha inscrito correctamente al curso")
        else:
            return super(UnirseAlCursoEstudianteView, self).form_valid(form)


# Vista del grafo
class GrafoEstudianteView(LoginRequiredMixin, ListView):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "Aprendeci/estudiante/grafo.html"

    def get_queryset(self):
        # TODO
        return serializers.serialize("json", self.model.objects.filter(grafo=2))


# Vista en detalle de un concepto
class ConceptoEstudianteView(LoginRequiredMixin, DetailView):
    context_object_name = "concepto"
    model = Concepto
    template_name = "Aprendeci/estudiante/concepto.html"

    def get_context_data(self, **kwargs):
        context = super(ConceptoEstudianteView, self).get_context_data(**kwargs)
        context['grafo_id'] = Concepto.objects.get(pk=self.kwargs['pk']).grafo.id
        return context