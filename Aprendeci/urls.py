from django.conf.urls import url

from Aprendeci import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^grafos/$', views.GrafoView.as_view(), name='grafos')
]