from django.conf.urls import patterns, url
from jirello import views


urlpatterns = (
    url(r'^$', views.main, name='main'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
)
