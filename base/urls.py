from django.conf.urls import patterns, url


urlpatterns = patterns('base.views',
                       # url(r'^$', 'home', name='home'),
                       url(r'^/?$', 'home', name='home'),
                       url(r'^login/?$', 'login', name='login'),
                       url(r'^create-account-from-file-by-admin-qsc/$', 'create_accounts', name='create-account')
)

