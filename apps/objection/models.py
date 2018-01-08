# coding=utf-8
from django.conf import settings
from django.db import models
from django.db.models import Q
from model_utils import Choices

from apps.base.models import Member, EducationalYear
from apps.course.management.commands.updatecourses import get_current_year
from apps.course.models import OfferedCourse


class Objection(models.Model):
    CATEGORY = Choices((0, 'a', u"------------"),
                       (1, 'b', u"تلاقی زمان کلاس"),
                       (2, 'c', u"تاریخ امتحان نامناسب"),
                       (3, 'd', u"عدم ارائه"),
                       (4, 'e', u"تعداد گروه کم"),
                       (6, 'g', u"غیره")
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

    TERM = Choices((1, 'fall', u'پاییز'), (2, 'spring', u'بهار'), (3, 'summer', u'تابستان'))

    term = models.PositiveSmallIntegerField(choices=TERM)
    year = models.ForeignKey(EducationalYear)

    @classmethod
    def get_available(cls, member):
        qs = Objection.objects.filter(term=settings.CURRENT_TERM, year=get_current_year())
        if member.is_superuser:
            return qs
        return qs.filter(Q(status__in=[1, 3, 4, 5]) | Q(sender=member))

    def get_serialized(self, member):
        try:
            reply = Reply.objects.filter(objection=self).last()
        except:
            reply = None
        return {
            'data_id': self.id,
            'category_id': self.category,
            'category_name': self.get_category_display(),
            'status_id': self.status,
            'status_name': self.get_status_display(),
            'metoos': self.like.count(),
            'metooed': member in self.like.all(),
            'offered_course': self.get_offered_course_id(),
            'second_course': self.get_second_course_id(),
            'course_name': self.course_name,
            'message': self.message,
            'can_me_too': not member.__eq__(self.sender),
            'reply': reply.text if reply else "",
            'reply_by': reply.author.username if reply else "",
        }


    def get_offered_course_id(self):
        if self.offered_course:
            return self.offered_course.get_name()
        return -1

    def get_second_course_id(self):
        if self.second_course:
            return self.second_course.get_name()
        return -1

    @property
    def requests(self):
        return 1 + self.like.count()

    # def validate_unique(self, exclude=None):
    #     from django.core.exceptions import ValidationError
    #
    #     super(Objection, self).validate_unique(exclude)

    class Meta:
        verbose_name = 'مشکل درسی'
        verbose_name_plural = 'مشکلات درسی'
        unique_together = ('category', 'offered_course', 'second_course', 'course_name', 'message')


class Reply(models.Model):
    text = models.TextField()
    objection = models.ForeignKey(Objection)
    author = models.ForeignKey(Member)

    def __str__(self):
        return "%s: %s"%(self.author, self.text)

    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ‌ها'
