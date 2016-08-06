from django.conf.urls import patterns, url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^$', 'home', name='home'),
    url(r'^/?$', views.index, name='home'),
    url(r'^members/?$', views.members, name='members'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^create-account-from-file-by-admin-qsc/$', views.create_accounts, name='create-account'),
    url(r'^change-password/?$', views.password_reset_change, name='password_reset_change'),
]
