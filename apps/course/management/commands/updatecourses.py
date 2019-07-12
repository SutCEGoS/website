import json

from django.core.management import BaseCommand

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from django.conf import settings

from apps.base.models import EducationalYear

from apps.course.models import Professor, Course, OfferedCourse


def get_current_year():
    return EducationalYear.objects.get_or_create(year=settings.CURRENT_YEAR)[0]


def create_course_offer(capacity, crs, dsc, exam_time, grp, prf):
    print("New offered course: ", grp, crs, prf)
    # FIXME does not exist error which is sueprstrange
    course_offer, new = OfferedCourse.objects.get_or_create(group_number=int(grp),
                                                            course=crs,
                                                            professor=prf,
                                                            term=settings.CURRENT_TERM,
                                                            year=get_current_year(),
                                                            defaults={
                                                                'capacity': capacity,
                                                                'details': dsc,
                                                                'exam_time': exam_time
                                                            })
    if not new:
        course_offer.capacity = capacity
        course_offer.details = dsc
        course_offer.exam_time = exam_time
        course_offer.save()

    return course_offer


def create_professor(instructor_name):
    prf, new = Professor.objects.get_or_create(name=instructor_name)
    return prf


def create_course(course_name, course_number):
    crs, new = Course.objects.get_or_create(course_number=course_number,
                                            defaults={'name': course_name})
    if not new:
        crs.name = course_name
        crs.save()
    return crs


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "kttp://term.inator.ir/courses/list/38/"
        data = urlopen(url)
        courses_list = json.loads(data.read().decode('utf8'))

        for item in courses_list:
            grp = item['course_id'].split('-')[-1]
            exam_time = item['exam_time']
            instructor_name = item['instructor']
            course_name = item['name']
            course_number = item['course_number']
            dsc = item['info']
            capacity = int(item['capacity'])

            prf = create_professor(instructor_name)
            crs = create_course(course_name, course_number)

            offer = create_course_offer(capacity, crs, dsc, exam_time, grp, prf)

        self.stdout.write(self.style.SUCCESS('Success!'))
