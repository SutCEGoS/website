from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.lock_disable, name='locker'),
    url(r'^test/$', views.lock, name='locker'),
    url(r'^add/$', views.add_new, name='add_rack'),
]
