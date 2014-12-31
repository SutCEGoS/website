# coding=utf-8
from django.db import models
from model_utils import Choices

from base.models import Member
from course.models import OfferedCourse


class Objection(models.Model):
    CATEGORY = Choices()
    STATUS = Choices((1, 'admin pending', u"منتظر تایید"), (2, 'unqualified', u"تایید نشده"),
                     (3, 'reply pending', u"منتظر پاسخ"), (4, 'ignored', u"مشاهده شده"),
                     (5, 'replied', u"پاسخ داده شده"))

    sender = models.ForeignKey(Member)
    like = models.ManyToManyField(Member, null=True, blank=True, related_name="liked_member")

    category = models.PositiveSmallIntegerField(choices=CATEGORY)

    offered_course = models.ForeignKey(OfferedCourse, null=True, blank=True, verbose_name=u'درس')
    second_course = models.ForeignKey(OfferedCourse, null=True, related_name='second', blank=True,
                                      verbose_name=u'تلاقی با')
    course_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'درس ارائه نشده')
    message = models.TextField(null=True, blank=True, verbose_name=u'متن')

    status = models.PositiveSmallIntegerField(choices=STATUS)


class Reply(models.Model):
    text = models.TextField()
    objection = models.ForeignKey(Objection)
    author = models.ForeignKey(Member)