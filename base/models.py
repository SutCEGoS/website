# coding=utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices

LEVEL = Choices((1, u'کارشناسی'), (2, u'ارشد'), (3, u'دکتری'))


class Logged(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        abstract = True


class Named(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"نام")

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class EducationalYear(models.Model):
    year = models.IntegerField()

    def __unicode__(self):
        return unicode(self.year)


class Member(AbstractUser):
    level = models.PositiveSmallIntegerField(choices=LEVEL, blank=True, null=True)
    start_year = models.ForeignKey('EducationalYear', blank=True, null=True)

    std_id = models.CharField(max_length=20, null=True, blank=True)

    password_changed = models.BooleanField(default=False)

    def has_voted(self, poll):
        from poll.models import Vote
        return Vote.objects.filter(member=self, choice__poll=poll).exists()
