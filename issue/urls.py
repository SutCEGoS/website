from django.conf.urls import patterns, url

urlpatterns = patterns('issue.views',
                       url(r'^requests/?$', 'requests', name='issues'),
                       url(r'^ajax/search$', 'search_issue', name='objection_ajax_search_issue'),
                       url(r'^ajax/items$', 'search_issue', name='get_objections_list_issue'),
                       url(r'^ajax/add$', 'add_issue', name='add_objection_issue'),
                       url(r'^ajax/me_too$', 'add_me_too', name='add_me_too_issue'),

)