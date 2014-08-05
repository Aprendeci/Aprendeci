from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from Aprendeci import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.acceder, name='acceder'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^acceder/$', 'django.contrib.auth.views.login', { 'template_name': 'Aprendeci/login.html' }, name='login'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^aprendeci/', include('Aprendeci.urls', namespace='Aprendeci')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)