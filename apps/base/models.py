# coding=utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel as Logged

LEVEL = Choices((1, u'کارشناسی'), (2, u'ارشد'), (3, u'دکتری'))


class Named(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"نام")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class EducationalYear(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


class Member(AbstractUser):
    level = models.PositiveSmallIntegerField(choices=LEVEL, blank=True, null=True)
    start_year = models.ForeignKey('EducationalYear', blank=True, null=True,
            on_delete=models.CASCADE)

    std_id = models.CharField(max_length=20, null=True, blank=True)

    password_changed = models.BooleanField(default=False)

    def has_voted(self, poll):
        from apps.poll.models import Vote
        return Vote.objects.filter(member=self, choice__poll=poll).exists()
