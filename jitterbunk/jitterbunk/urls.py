from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('', include('bunk.urls')),
    url(r'^bunks/', include('bunk.urls', namespace="bunk")),
    url(r'^admin/', include(admin.site.urls)),
)
