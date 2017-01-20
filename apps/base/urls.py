from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^change-password/?$', views.password_reset_change, name='password_reset_change'),
    url(r'^$', views.index, name='home'),
    # url('^password_reset/', auth_views.password_reset, {'template_name': 'password_reset/password_reset_form.html'}, name='password_reset'),
    # url('^', include('django.contrib.auth.urls')),
]
