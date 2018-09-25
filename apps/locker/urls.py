from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$',views.lock,name='locker'),
	url(r"^(?P<locker_id>[0-17]+)/show/$", views.show_locker_condition, name='show-locker'),
]
