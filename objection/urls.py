from django.conf.urls import patterns, url

urlpatterns = patterns('objection.views',
                       url(r'^requests/?$', 'requests', name='requests'),
                       url(r'api/v1/search', 'search', name='objection_api_search')

)