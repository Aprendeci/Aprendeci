from django.conf.urls import url

from Aprendeci import views

urlpatterns = [
    # Estudiante
    url(r'^perfilEstudiante/$', views.PerfilEstudianteView.as_view(), name='perfilEstudiante'),
    url(r'^cursos/$', views.CursosEstudianteView.as_view(), name='listaCursos'),
    url(r'^unirse/(?P<id>[0-9]+)/$', views.UnirseAlCursoEstudianteView.as_view(), name='unirseCurso'),
    url(r'^estudiante/curso/(?P<id>[0-9]+)/$', views.CursoEstudianteView.as_view(), name='cursoEstudiante'),
    url(r'^estudiante/concepto/(?P<pk>[0-9]+)/$', views.ConceptoEstudianteView.as_view(), name='conceptoEstudiante'),
    # Profesor
    url(r'^perfilProfesor/$', views.PerfilProfesorView.as_view(), name='perfilProfesor'),
    url(r'^cursosProfesor/$', views.CursosProfesorView.as_view(), name='cursos'),
    url(r'^grafos/$', views.GrafosView.as_view(), name='grafos'),
    url(r'^grafos/(?P<id>[0-9]+)/$', views.GrafoView.as_view(), name='grafo'),
    url(r'^grafos/union$', views.UnirGrafosView.as_view(), name='unirgrafos'),
    url(r'^conceptos/(?P<id>[0-9]+)/$', views.ConceptosGrafoView.as_view(), name='conceptos'),
    url(r'^concepto/(?P<pk>[0-9]+)/$', views.ConceptoView.as_view(), name='concepto'),
]