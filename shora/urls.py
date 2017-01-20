from django.conf.urls import include, url
from django.contrib import admin
from password_reset.views import recover_done, recover, reset_done, reset
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('password_reset.urls')),
    url(r'^accounts/', include([
        url(r'^recover/(?P<signature>.+)/$', recover_done, name='password_reset_sent'),
        url(r'^recover/$', recover, name='password_reset_recover'),
        url(r'^reset/done/$', reset_done, name='password_reset_done'),
        url(r'^reset/(?P<token>[\w:-]+)/$', reset, name='password_reset_reset'),
    ])),
]

urlpatterns += [
    url(r'^', include('apps.base.urls')),
    url(r'^objections/', include('apps.objection.urls')),
    url(r'^issues/', include('apps.issue.urls')),
    url(r'^polls/', include('apps.poll.urls')),
    url(r'^events/', include('apps.event.urls')),
    url(r'^announcements/', include('apps.announcements.urls')),
    url(r'^pages/', include('apps.pages.urls')),

    # Plugins
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^hijack/', include('hijack.urls')),
]
