from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.all_events, name='all-events'),
    url(r'^get-event/$', views.get_event, name='get-event'),
    url(r'^register/$', views.register_in_event, name='register-in-event'),
    url(r'^payment/(?P<event_id>[0-9]*)$', views.payment, name='payment'),
    url(r'^payment-result/(?P<donate_id>[0-9]*)$', views.payment_result),

]
