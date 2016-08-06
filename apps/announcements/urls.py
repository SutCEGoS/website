from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^/?$", views.all_announcements, name='all-announcements'),
    url(r"^(?P<announcement_id>[0-9]+)/show/$", views.show_announcement, name='show-announcement')
]