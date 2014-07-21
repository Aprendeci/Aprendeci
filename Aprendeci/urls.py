from django.conf.urls import url

from Aprendeci import views

urlpatterns = [
    url(r'^grafos/$', views.GrafosView.as_view(), name='grafos'),
    url(r'^grafos/(?P<id>[0-9])/$', views.GrafoView.as_view(), name='grafo'),
    url(r'^conceptos/(?P<id>[0-9])/$', views.ConceptosGrafoView.as_view(), name='conceptos'),
    url(r'^concepto/(?P<pk>[0-9])/$', views.ConceptoView.as_view(), name='concepto'),
]