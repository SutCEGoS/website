from django.conf.urls import patterns, url

urlpatterns = patterns('poll.views',
                       url(r'^$', 'all_polls', name='all-polls'),
                       url(r'^get-poll/$', 'get_poll', name='get-poll'),
)
