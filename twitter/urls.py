from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html$', views.index, name='index1'),
    url(r'^New.html$', views.PostIndex, name='PostIndex'),
    #url(r'^graphics$', views.graphico, name='graphics'),

]