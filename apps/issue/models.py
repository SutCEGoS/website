# coding=utf-8
from django.db import models
from django.db.models import Q
from model_utils import Choices

from apps.base.models import Member, Logged


class Issue(models.Model):
    CATEGORY = Choices((0, 'a', u"------------"),
                       (1, 'b', u"شورای صنفی"),
                       (3, 'c', u"لابی"),
                       (5, 'd', u"کتابخانه"),
                       (7, 'e', u"نمازخانه"),
                       (9, 'f', u"کلاس ها"),
                       (11, 'g', u"سالن مطالعه"),
                       (13, 'h', u"سایت"),
                       (15, 'i', u"اغذیه فروشی"),
                       (17, 'k', u"ساختمان دانشکده"),
                       (19, 'j', u"تاسیسات"),
                       (30, 'l', u"سایر موارد"),

    )
    STATUS = Choices((1, 'admin pending', u"منتظر تایید"), (2, 'unqualified', u"تایید نشده"),
                     (3, 'reply pending', u"منتظر پاسخ"), (4, 'ignored', u"مشاهده شده"),
                     (5, 'replied', u"پاسخ داده شده"))

    sender = models.ForeignKey(Member, null=True, blank=True)
    like = models.ManyToManyField(Member, null=True, blank=True, related_name="issue_liked_member")
    title = models.CharField(max_length=63)
    category = models.PositiveSmallIntegerField(choices=CATEGORY)
    message = models.TextField(null=True, blank=True, verbose_name=u'متن')
    status = models.PositiveSmallIntegerField(choices=STATUS)
    reply = models.ForeignKey('IssueReply', null=True, blank=True)

    @classmethod
    def get_available(cls, member):
        if member.is_superuser:
            return Issue.objects.all()
        return Issue.objects.filter(Q(status__in=[1, 3, 4, 5]) | Q(sender=member))

    def get_serialized(self, member):
        reply = self.reply
        return {
            'data_id': self.id,
            'title': self.title,
            'category_id': self.category,
            'category_name': self.get_category_display(),
            'status_id': self.status,
            'status_name': self.get_status_display(),
            'metoos': self.like.count(),
            'metooed': member in self.like.all(),
            'message': self.message,
            'can_me_too': not member.__eq__(self.sender),
            'reply': reply.text if reply else "",
            'reply_by': reply.author.get_full_name() if reply else "",
        }

    @property
    def requests(self):
        return 1 + self.like.count()


class IssueReply(Logged):
    text = models.TextField()
    author = models.ForeignKey(Member)

    def __str__(self):
        return "%s: %s"%(self.author, self.text)