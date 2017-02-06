from django.conf.urls import include, patterns, url
from jirello import views


urlpatterns = patterns(
    '',
    url(r'^$', views.main, name='main'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^project-new/$', views.project_new, name='project-new'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(?P<projectmodel_id>[0-9]+)/',
        # ALL CURRENT PROJECT URL
        include(patterns(
            '',
            url(r'^$', views.project_detail, name='project-detail'),
            url(r'^search/',
                views.TaskSearchView.as_view(),
                name='task-search'),
            url(r'^project-edit/$', views.project_edit, name='project-edit'),
            url(r'^task-new/$', views.task_new, name='task-new'),
            url(r'^sprint-new/$', views.sprint_new, name='sprint-new'),
            url(r'^sprint/(?P<sprint_id>[0-9]+)/$',
                views.sprint_detail,
                name='sprint-detail'),
            url(r'^sprint/(?P<sprint_id>[0-9]+)/edit/$',
                views.sprint_edit,
                name='sprint-edit'),
            url(r'^task/(?P<task_id>[0-9]+)/$',
                views.task_detail,
                name='task-detail'),
            url(r'^task/(?P<task_id>[0-9]+)/edit/$',
                views.task_edit,
                name='task-edit'),
        ))),
)
