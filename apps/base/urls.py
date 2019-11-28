from django.conf.urls import url, include
from django.urls import path

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
    url(r'^charge/checkout/$', views.checkout_view, name='checkout'),
    url(r'^charge/checkout/list$', views.checkout_list_view, name='checkout_list'),
    url(r'charge/checkout/action/(?P<req_id>[0-9]+)/(?P<action>[2-3]+)', views.checkout_action, name='checkout_action'),
    url(r'^charge/$', views.charge_menu, name='charge_menu'),
    url(r'^history/$', views.history, name='history'),
    url(r'^charge/payment/(?P<transaction_id>[0-9]+)$', views.payment, name='payment'),
    url(r'^charge/verify/$', views.verify, name='verify'),

    # url('^password_reset/', auth_views.password_reset, {'template_name': 'password_reset/password_reset_form.html'}, name='password_reset'),
    # url('^', include('django.contrib.auth.urls')),
]
