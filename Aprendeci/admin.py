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
        obj.profesor = request.user
        obj.save()


# Signals
def crear_estudiante(sender, instance, **kwargs):
    if len(Estudiante.objects.filter(usuario__pk=instance.pk)) == 0:
        nuevoEstudiante = Estudiante(usuario=instance)
        nuevoEstudiante.save()

post_save.connect(crear_estudiante, sender=User, dispatch_uid="crear_estudiante")


# Registro de modelos
admin.autodiscover()
admin.site.register(Concepto, ConceptoAdmin)
admin.site.register(Grafo)
admin.site.register(Recurso)
admin.site.register(Curso, CursoAdmin)

# Configuracion del admin
admin.site.login = login_required(admin.site.login)