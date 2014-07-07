from django.conf.urls import url

from Aprendeci import views

urlpatterns = [
    url(r'^grafos/$', views.GrafosView.as_view(), name='grafos'),
    url(r'^grafos/(?P<id>[0-9])/$', views.GrafoView.as_view(), name='grafo'),
]