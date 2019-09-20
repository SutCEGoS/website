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
    url(r'^charge/cash/$', views.charge_cash, name='charge_cash'),
    url(r'^charge/credit/$', views.charge_credit, name='charge_credit'),
    url(r'^charge/$', views.charge_menu, name='charge_menu'),
    url(r'^charge/payment/(?P<transaction_id>[0-9]+)$', views.payment, name='payment'),
    url(r'^charge/verify/$', views.verify, name='verify'),
    # url('^password_reset/', auth_views.password_reset, {'template_name': 'password_reset/password_reset_form.html'}, name='password_reset'),
    # url('^', include('django.contrib.auth.urls')),
]
