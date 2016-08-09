from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[a-zA-Z_0-9-]+)/$', views.page_visit, name='page_visit')
]
