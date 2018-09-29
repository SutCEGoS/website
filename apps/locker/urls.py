from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$',views.lock,name='locker'),
    url(r'^ajax/add$', views.add, name='add_rack'),
]
