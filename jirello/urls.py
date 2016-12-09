from django.conf.urls import patterns, url
from jirello import views


urlpatterns = (
    url(r'^$', views.main, name='main'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^new_project/$', views.new_project, name='new_project'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(?P<projectmodel_id>[0-9]+)/$',
        views.projects_detail,
        name='projects_detail'),
)
