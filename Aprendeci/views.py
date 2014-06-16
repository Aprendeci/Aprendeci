from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from Aprendeci.models import Concepto

class JSONResponseMixin(object):
    def get_queryset(self):
        return serializers.serialize("json", self.model.objects.all())

class IndexView(JSONResponseMixin, ListView):
    context_object_name = "concepto_list"
    model = Concepto
    template_name = "Aprendeci/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)