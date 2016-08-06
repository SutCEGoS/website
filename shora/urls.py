from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('password_reset.urls')),
]

urlpatterns += [
    url(r'^', include('apps.base.urls')),
    url(r'^courses/', include('apps.course.urls')),
    url(r'^objections/', include('apps.objection.urls')),
    url(r'^issues/', include('apps.issue.urls')),
    url(r'^polls/', include('apps.poll.urls')),
    url(r'^events/', include('apps.event.urls')),
    url(r'^announcements/', include('apps.announcements.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]
