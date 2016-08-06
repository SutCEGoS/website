from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.all_polls, name='all-polls'),
    url(r'^get-poll/$', views.get_poll, name='get-poll'),
    url(r'^submit-vote/$', views.submit_vote, name='submit-vote'),
]
