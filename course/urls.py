from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^update-courses-list-from-term-inatot-ppqwrtopf/$', views.update_courses_list, name='update-courses-list')
]
