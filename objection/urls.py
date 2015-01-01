from django.conf.urls import patterns, url

urlpatterns = patterns('objection.views',
                       url(r'^requests/?$', 'requests', name='requests'),
                       url(r'ajax/search', 'search', name='objection_ajax_search')

)