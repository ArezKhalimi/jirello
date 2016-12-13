from django.conf.urls import include, patterns, url
from jirello import views


urlpatterns = patterns(
    '',
    url(r'^$', views.main, name='main'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^new_project/$', views.new_project, name='new_project'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(?P<projectmodel_id>[0-9]+)/',
        # ALL CURRENT PROJECT URL
        include(patterns(
            '',
            url(r'^$', views.projects_detail, name='project_detail'),
            url(r'^edit_project/$', views.edit_project, name='edit_project'),
            url(r'^new_sprint/$', views.new_sprint, name='new_sprint')))
        ),
)
