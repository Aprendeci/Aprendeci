from django.contrib.auth.decorators import login_required
from django.contrib import admin
from Aprendeci.models import *


# Custom admin models
class ConceptoAdmin(admin.ModelAdmin):
    exclude = ("x", "y",)


class CursoAdmin(admin.ModelAdmin):
    exclude = ("profesor", "estudiantes",)

    def save_model(self, request, obj, form, change):
        obj.profesor = request.user
        obj.save()


# Registro de modelos
admin.autodiscover()
admin.site.register(Concepto, ConceptoAdmin)
admin.site.register(Grafo)
admin.site.register(Recurso)
admin.site.register(Curso, CursoAdmin)

# Configuracion del admin
admin.site.login = login_required(admin.site.login)