from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('base.views',
                       # url(r'^$', 'home', name='home'),
                       url(r'^/?$', 'home', name='home'),
                       url(r'^login/?$', 'login', name='login'),
                       url(r'^logout/?$', 'logout', name='logout'),
                       url(r'^create-account-from-file-by-admin-qsc/$', 'create_accounts', name='create-account'),
                       url(r'^change-password/?$', 'password_reset_change', name='password_reset_change'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

