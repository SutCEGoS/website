from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$',views.lock,name='locker'),
    url(r'^add/$', views.add_new, name='add_rack'),
	url(r'^payment/(?P<rack_id>[0-9]+)$', views.payment, name='pay'),
	url(r'^payment-result/', views.payment_result),

]
