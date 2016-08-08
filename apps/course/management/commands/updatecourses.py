import json

from django.core.management import BaseCommand

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from django.conf import settings

from base.models import EducationalYear

from course.models import Professor, Course, OfferedCourse


def get_current_year():
    return EducationalYear.objects.get_or_create(year=settings.CURRENT_YEAR)[0]


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "http://term.inator.ir/courses/list/38/"
        data = urlopen(url)
        courses_list = json.loads(data.read().decode('utf8'))
        for item in courses_list:
            grp = item['course_id'].split('-')[-1]
            exam_time = item['exam_time']
            prf = item['instructor']
            prf = Professor.objects.get_or_create(name=prf)
            crs = item['course_number']
            crs_name = item['name']
            crs = Course.objects.get_or_create(course_number=crs,
                                               name=crs_name, )
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
        self.stdout.write(self.style.SUCCESS('Success!'))