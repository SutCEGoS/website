import json
# import urllib2

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from apps.base.models import EducationalYear

from apps.course.models import Professor, Course, OfferedCourse


def get_current_year():
    return EducationalYear.objects.get_or_create(year=settings.CURRENT_YEAR)[0]


@login_required
def update_courses_list(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    url = "http://term.inator.ir/courses/list/38/"
    data = urlopen(url)
    courses_list = json.loads(data.read().decode('utf-8'))
    for item in courses_list:
        grp = item['course_id'].split('-')[-1]
        exam_time = item['exam_time']
        prf = item['instructor']
        prf = Professor.objects.get_or_create(name=prf)
        crs = item['course_number']
        crs_name = item['name']
        crs = Course.objects.get_or_create(course_number=crs)
        dsc = item['info']
        capacity = int(item['capacity'])
        try:
            obj = OfferedCourse.objects.get(group_number=int(grp),
                                            course=crs[0],
                                            professor=prf[0],
                                            term=settings.CURRENT_TERM,
                                            year=get_current_year(), )
            obj.capacity = capacity
            obj.details = dsc
            obj.exam_time = exam_time
        except OfferedCourse.DoesNotExist:
            obj = OfferedCourse.objects.create(group_number=int(grp),
                                               course=crs[0],
                                               professor=prf[0],
                                               term=settings.CURRENT_TERM,
                                               year=get_current_year(),

                                               capacity=capacity,
                                               details=dsc,
                                               exam_time=exam_time, )
    return HttpResponse("success!")
