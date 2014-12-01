from django import forms
from django.contrib.auth.models import User, Group
from django.views.generic import FormView
from Aprendeci.models import Estudiante, Profesor
from .viewsGeneral import *

# Class based views


# Vista principal
class PerfilAdminView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'Aprendeci/administrador/perfil.html'


# Formulario para agregar un usuario
class AgregarUsuarioForm(forms.Form):
    ESTUDIANTE = 'E'
    PROFESOR = 'P'
    TIPOS_USUARIO = (
        (ESTUDIANTE, 'Estudiante'),
        (PROFESOR, 'Profesor'),
    )

    nombreUsuario = forms.CharField(label='Nombre de usuario', max_length=100)
    clave = forms.CharField(label='Clave', widget=forms.PasswordInput)
    confirmacionClave = forms.CharField(label='Confirmar clave', widget=forms.PasswordInput)
    correo = forms.EmailField(label='Correo electrónico')
    nombre = forms.CharField(label='Nombre', max_length=50)
    apellido = forms.CharField(label='Apellido', max_length=50)
    tipo = forms.ChoiceField(label='Tipo', choices=TIPOS_USUARIO)

    def clean_confirmacionClave(self):
        clave1 = self.cleaned_data.get("clave")
        clave2 = self.cleaned_data.get("confirmacionClave")
        if clave1 and clave2 and clave1 != clave2:
            raise forms.ValidationError("Las claves no coinciden")
        return clave2

    def agregar_usuario(self):
        nombreUsuario = self.cleaned_data['nombreUsuario']
        clave = self.cleaned_data['clave']
        correo = self.cleaned_data['correo']
        nombre = self.cleaned_data['nombre']
        apellido = self.cleaned_data['apellido']
        tipo = self.cleaned_data['tipo']

        # Crear el usuario
        usuario = User.objects.create_user(username=nombreUsuario, email=correo, password=clave)
        usuario.first_name = nombre
        usuario.last_name = apellido

        # Crear el perfil
        if tipo == self.ESTUDIANTE:
            estudiante = Estudiante(usuario=usuario)
            estudiante.save()

            usuario.groups.add(Group.objects.get(name="Estudiantes"))
        elif tipo == self.PROFESOR:
            profesor = Profesor(usuario=usuario)
            profesor.save()

            usuario.groups.add(Group.objects.get(name="Profesores"))

        usuario.save()


class AgregarUsuarioView(LoginRequiredMixin, SuperuserRequiredMixin, FormView):
    form_class = AgregarUsuarioForm
    template_name = "Aprendeci/administrador/agregarUsuario.html"
    success_url = "/aprendeci/usuario/agregar/exito/"

    def form_invalid(self, form):
        return super(AgregarUsuarioView, self).form_invalid(form)

    def form_valid(self, form):
        form.agregar_usuario()
        return super(AgregarUsuarioView, self).form_valid(form)


class AgregarUsuarioExitoView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = "Aprendeci/administrador/agregarUsuarioExito.html"