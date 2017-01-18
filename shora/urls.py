from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('password_reset.urls')),
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
