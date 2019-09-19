from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^change-password/?$', views.password_reset_change, name='password_reset_change'),
    url(r'^$', views.index, name='home'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^complete_profile', views.complete_profile, name='complete_profile'),
    url(r'^under_construction/', views.under_construction, name='under_construction'),
    url(r'^charge/cash', views.charge_cash, name='charge_cash'),
    url(r'^charge/', views.charge_menu, name='charge_menu'),
    # url('^password_reset/', auth_views.password_reset, {'template_name': 'password_reset/password_reset_form.html'}, name='password_reset'),
    # url('^', include('django.contrib.auth.urls')),
]
