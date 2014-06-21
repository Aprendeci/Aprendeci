from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login', { 'template_name': 'Aprendeci/login.html' }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^aprendeci/', include('Aprendeci.urls', namespace='Aprendeci'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)