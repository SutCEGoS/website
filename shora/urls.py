from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('password_reset.urls')),
)

urlpatterns += patterns('',
                        url(r'^', include('base.urls')),
                        url(r'^courses/', include('course.urls')),
                        url(r'^objections/', include('objection.urls')),
                        url(r'^issues/', include('issue.urls')),
                        url(r'^polls/', include('poll.urls')),
                        url(r'^events/', include('event.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
)
