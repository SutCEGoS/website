from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^requests/?$', views.requests, name='requests'),
    url(r'^ajax/search$', views.search, name='objection_ajax_search'),
    url(r'^ajax/courses$', views.get_courses, name='get_courses_list'),
    url(r'^ajax/objections$', views.search, name='get_objections_list'),
    url(r'^ajax/add$', views.add_objection, name='add_objection'),
    url(r'^ajax/me_too$', views.add_me_too, name='add_me_too'),

]
