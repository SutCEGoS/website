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

    card_number = models.CharField(null=True, blank=True, max_length=20)
    sheba = models.CharField(null=True, blank=True, max_length=30, default="")

    def has_voted(self, poll):
        from apps.poll.models import Vote
        return Vote.objects.filter(member=self, choice__poll=poll).exists()

    def __str__(self):
        if self.get_full_name() is not None:
            return self.get_full_name()
        else:
            return self.username

    def get_card_number_display(self):
        if len(self.card_number) != 16:
            return self.card_number
        return "%s-%s-%s-%s" % (self.card_number[0:4], self.card_number[4:8], self.card_number[8:12], self.card_number[12:])


class Transaction(models.Model):
    TYPE_CHOICES = (
        (1, "شارژ نقدی"),
        (2, "شارژ آنلاین"),
        (3, "انتقال وجه"),
        (4, "استفاده از خدمات شورا"),
        (5, "تسویه حساب")
    )

    origin = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, verbose_name="مبدا", related_name="origin")
    destination = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, verbose_name="مقصد",
                                    related_name="destination")
    amount = models.IntegerField(verbose_name="مبلغ")
    type = models.IntegerField(verbose_name="نوع تراکنش", choices=TYPE_CHOICES)
    is_successfully = models.BooleanField(verbose_name="موفقیت", default=False)
    Authority = models.CharField(max_length=512, null=True)
    data = models.CharField(max_length=512, null=True, verbose_name="توضیحات")
    time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان")

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"

    def __str__(self):
        if self.type == 1:
            return "شارژ نقدی حساب %s به میزان %d تومان" % (self.destination, self.amount)
        elif self.type == 2:
            return "شارژ آنلاین حساب %s به میزان %d تومان" % (self.destination, self.amount)
        elif self.type == 3:
            return "انتقال %d تومان از حساب %s به حساب %s" % (self.amount, self.origin, self.destination)
        elif self.type == 4:
            return "استفاده از خدمات شورا توسط %s به میزان %d تومان" % (self.origin, self.amount)


class CheckoutRequest(models.Model):
    STATUS_CHOICES = (
        (1, "درخواست شده"),
        (2, "انجام شده"),
        (3, "لغو شده"),
    )
    user = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="کاربر")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درخواست")
    status = models.IntegerField(verbose_name="وضعیت", choices=STATUS_CHOICES, default=1)

    class Meta:
        verbose_name = "درخواست تسویهٔ حساب"
        verbose_name_plural = "درحواست‌های تسویهٔ حساب"
