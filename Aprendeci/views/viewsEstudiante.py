from django.core import serializers
from django.views.generic import DetailView, ListView, TemplateView
from Aprendeci.models import Concepto
from .viewsGeneral import *


# Class based views

# Vista principal
class PerfilEstudianteView(LoginRequiredMixin, TemplateView):
    template_name = 'Aprendeci/estudiante/perfil.html'


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