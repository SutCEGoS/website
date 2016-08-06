from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^members/?$', views.members, name='members'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^create-account-from-file-by-admin-qsc/$', views.create_accounts, name='create-account'),
    url(r'^change-password/?$', views.password_reset_change, name='password_reset_change'),
    url(r'^$', views.index, name='home'),
]
