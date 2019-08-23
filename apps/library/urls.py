from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.library_index, name='locker'),
]
