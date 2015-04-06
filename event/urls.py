from django.conf.urls import patterns, url

urlpatterns = patterns('event.views',
                       url(r'^$', 'all_events', name='all-events'),
                       url(r'^get-event/$', 'get_event', name='get-event'),
                       url(r'^register/$', 'register_in_event', name='register-in-event'),

)
