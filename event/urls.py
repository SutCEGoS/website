from django.conf.urls import patterns, url

urlpatterns = patterns('event.views',
                       url(r'^$', 'all_events', name='all-events'),
                       url(r'^get-event/$', 'get_event', name='get-event'),
                       url(r'^register/$', 'register_in_event', name='register-in-event'),
                       url(r'^payment/(?P<event_id>[0-9]*)$', 'payment', name='payment'),
                       url(r'^payment-result/(?P<donate_id>[0-9]*)$', 'payment_result'),

)
