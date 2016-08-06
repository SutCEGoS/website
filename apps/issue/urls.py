from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^requests/?$', views.requests, name='issues'),
    url(r'^ajax/search$', views.search_issue, name='objection_ajax_search_issue'),
    url(r'^ajax/items$', views.search_issue, name='get_objections_list_issue'),
    url(r'^ajax/add$', views.add_issue, name='add_objection_issue'),
    url(r'^ajax/me_too$', views.add_me_too, name='add_me_too_issue'),
]
