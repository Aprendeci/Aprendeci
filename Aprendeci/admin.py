from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.db.models.signals import post_save
from Aprendeci.models import *


# Custom admin models
class ConceptoAdmin(admin.ModelAdmin):
    exclude = ("x", "y",)


class CursoAdmin(admin.ModelAdmin):
    exclude = ("profesor", "estudiantes",)

    def save_model(self, request, obj, form, change):
        obj.profesor = request.user.profesor
        obj.save()


# Registro de Estudiante
admin.autodiscover()
admin.site.register(Concepto, ConceptoAdmin)
admin.site.register(Grafo)
admin.site.register(Recurso)
admin.site.register(Curso, CursoAdmin)

# Configuracion del admin
admin.site.login = login_required(admin.site.login)