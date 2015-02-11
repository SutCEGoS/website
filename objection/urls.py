from django.conf.urls import patterns, url

urlpatterns = patterns('objection.views',
                       url(r'^requests/?$', 'requests', name='requests'),
                       url(r'^ajax/search$', 'search', name='objection_ajax_search'),
                       url(r'^ajax/courses$', 'get_courses', name='get_courses_list'),
                       url(r'^ajax/objections$', 'search', name='get_objections_list'),
                       url(r'^ajax/add$', 'add_objection', name='add_objection'),
                       url(r'^ajax/me_too$', 'add_me_too', name='add_me_too'),

)