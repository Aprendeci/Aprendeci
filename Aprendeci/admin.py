from django.contrib import admin
from Aprendeci.models import Concepto

class ConceptoAdmin(admin.ModelAdmin):
    exclude = ("x", "y",)

admin.site.register(Concepto, ConceptoAdmin)