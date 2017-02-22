from django.conf.urls import url

from . import views

app_name = 'classify'
urlpatterns = [
    url(r'^$', views.classifying, name='index'),
    url(r'^results/(?P<pk>[0-9]+)$', views.results, name='results'),
]