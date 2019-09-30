from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.lock, name='locker'),
    url(r'^add/$', views.add_new, name='add_rack'),
]
