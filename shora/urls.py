from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        url(r'^', include('base.urls')),
                        url(r'^courses/', include('course.urls')),
                        url(r'^objections/', include('objection.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
