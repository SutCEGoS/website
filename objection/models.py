# coding=utf-8
from django.db import models
from django.db.models import Q
from model_utils import Choices

from base.models import Member
from course.models import OfferedCourse


class Objection(models.Model):
    CATEGORY = Choices(
                        (2, 'a', u"تلاقی زمان کلاس"),
                        (3, 'b', u"تاریخ امتحان نامناسب"),
                        (4, 'c', u"عدم ارائه درس"),
                        (5, 'd', u"تعداد گروه کم"),
                        (6, 'e', u"عدم صلاحیت استاد برای ارائه درس"),
                        (7, 'f', u"غیره")
    )
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

    @classmethod
    def get_available(cls, member):
        if member.is_superuser:
            return Objection.objects.all()
        if member.groups.filter(name='Replier').exists():
            return Objection.objects.filter(status__ge=3)
        return Objection.objects.filter(Q(status__ge=3) | Q(sender=member))

    def get_serialized(self, member):
        return {
            'data_id': self.id,
            'category_id': self.category,
            'category_name': self.get_category_display(),
            'status_id': self.status,
            'status_name': self.get_status_display(),
            'metoos': self.like.count(),
            'metooed': member in self.like.all(),
            'offered_course': self.offered_course.id,
            'second_course': self.second_course.id,
            'course_name': self.course_name,
            'message': self.message,
            'reply': 'this request ic chert',
            'reply-by': 'amin',
        }


class Reply(models.Model):
    text = models.TextField()
    objection = models.ForeignKey(Objection)
    author = models.ForeignKey(Member)