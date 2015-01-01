from django.conf.urls import patterns, url

urlpatterns = patterns('objection.views',
                       url(r'^requests/?$', 'requests', name='requests'),
                       url(r'ajax/search', 'search', name='objection_api_search'),
                       url(r'ajax/courses', 'get_courses', name='get_courses_list'),
)