# coding=utf-8
from django.db import models
from model_utils import Choices

from base.models import Named, EducationalYear


class Professor(Named):
    pass


class Field(Named):
    pass


class Course(Named):
    course_number = models.CharField(max_length=10, unique=True)


class OfferedCourse(models.Model):
    TERM = Choices((1, 'fall', u'پاییز'), (2, 'spring', u'بهار'), (3, 'summer', u'تابستان'))

    course = models.ForeignKey(Course)
    professor = models.ForeignKey(Professor)
    group_number = models.SmallIntegerField(default=1)
    term = models.PositiveSmallIntegerField(choices=TERM)
    year = models.ForeignKey(EducationalYear)
    exam_time = models.CharField(max_length=255)
    capacity = models.IntegerField()
    details = models.CharField(max_length=1023)

    class Meta:
        unique_together = ("course", "group_number", "term", "year")

    def __str__(self):
        return "%s-%d - %s - %s  " % (
            str(self.course.course_number), self.group_number, str(self.course), str(self.professor))

    def get_name(self):
        return u"%s گروه %d استاد %s" % (self.course.name, self.group_number, self.professor)