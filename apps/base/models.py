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

    cash = models.IntegerField(default=0)

    password_changed = models.BooleanField(default=False)

    def has_voted(self, poll):
        from apps.poll.models import Vote
        return Vote.objects.filter(member=self, choice__poll=poll).exists()

    def __str__(self):
        if self.get_full_name() is not None:
            return self.get_full_name()
        else:
            return self.username


class Transaction(models.Model):
    TYPE_CHOICES = (
        (1, "شارژ نقدی"),
        (2, "شارژ آنلاین"),
        (3, "انتقال وجه"),
        (4, "استفاده از خدمات شورا")
    )

    origin = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, verbose_name="مبدا")
    destination = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, verbose_name="مقصد")
    amount = models.IntegerField(verbose_name="مبلغ")
    type = models.IntegerField(verbose_name="نوع تراکنش", choices=TYPE_CHOICES)
    is_successfully = models.BooleanField(verbose_name="موفقیت", default=False)
