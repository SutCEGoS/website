from django.conf.urls import patterns, url

urlpatterns = patterns('course.views',
                       url(r'^update-courses-list-from-term-inatot-ppqwrtopf/$', 'update_courses_list',
                           name='update-courses-list')
)