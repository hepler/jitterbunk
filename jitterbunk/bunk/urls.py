from django.conf.urls import patterns, url
from bunk import views

urlpatterns = patterns('',
    url(r'^login/$', 'bunk.views.login_user'),
    url(r'^logout/$', 'bunk.views.logout_user'),
    url(r'^$', views.index, name='index'),
    # view user's bunks
    url(r'^(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
    url(r'^bunk$', views.bunk_form, name='bunk_form'),
    url(r'^bunked$', views.bunked, name='bunked'),
)
