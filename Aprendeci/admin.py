from django.contrib import admin
from Aprendeci.models import *

class ConceptoAdmin(admin.ModelAdmin):
    exclude = ("x", "y",)

admin.site.register(Concepto, ConceptoAdmin)
admin.site.register(Grafo)