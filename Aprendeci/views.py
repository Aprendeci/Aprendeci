import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.generic import ListView
from Aprendeci.models import Concepto

class JSONResponseMixin(object):
    def get_queryset(self):
        return serializers.serialize("json", self.model.objects.all())

class IndexView(JSONResponseMixin, ListView):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = 'Aprendeci/index.html'