from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect
import logging

# Configuracion general


logger = logging.getLogger('aprendeci')


# Mixins


# Mixin para la autenticacion
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


# Funciones

@login_required
def acceder(request):
    if request.user.groups.filter(name="Profesores").exists():
        return redirect("Aprendeci:perfilProfesor")
    elif request.user.groups.filter(name="Estudiantes").exists():
        return redirect("Aprendeci:perfilEstudiante")
    else:
        return redirect("admin:index")

# Desloguearse
def logoutView(request):
    logout(request)
    return redirect("login")