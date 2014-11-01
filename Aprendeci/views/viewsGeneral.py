from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
import logging

# Configuracion general
from django.views.generic import TemplateView


logger = logging.getLogger('aprendeci')


# Mixins


# Mixin para la autenticacion
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


# Mixin para la proteccion de las paginas del administrador
class SuperuserRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/aprendeci/denegado'))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)


# Mixin para la proteccion de las paginas del profesor
class ProfesorRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Profesores').count() != 0, login_url='/aprendeci/denegado'))
    def dispatch(self, *args, **kwargs):
        return super(ProfesorRequiredMixin, self).dispatch(*args, **kwargs)


# Mixin para la proteccion de las paginas del estudiante
class EstudianteRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Estudiantes').count() != 0, login_url='/aprendeci/denegado'))
    def dispatch(self, *args, **kwargs):
        return super(EstudianteRequiredMixin, self).dispatch(*args, **kwargs)


# Funciones

@login_required
def acceder(request):
    if request.user.is_superuser:
        return redirect("Aprendeci:perfilAdmin")
    elif request.user.groups.filter(name="Profesores").exists():
        return redirect("Aprendeci:perfilProfesor")
    elif request.user.groups.filter(name="Estudiantes").exists():
        return redirect("Aprendeci:perfilEstudiante")
    else:
        return redirect("admin:index")


# Desloguearse
def logoutView(request):
    logout(request)
    return redirect("login")


# Permisos insuficientes
class PermisosInsuficientesView(TemplateView):
    template_name = "Aprendeci/permisosInsuficientes.html"