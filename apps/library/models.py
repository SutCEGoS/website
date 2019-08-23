from django.db.models import *


class Book(Model):
    name = CharField(verbose_name="نام", max_length=100)
    author = CharField(verbose_name="نویسنده", max_length=100, null=True)
    translator = CharField(verbose_name="مترجم", max_length=100, null=True)
    publication = CharField(verbose_name="ناشر", max_length=100, null=True)
    image = ImageField(verbose_name="تصویر کتاب")

    def __str__(self):
        return "%s(انتشارات: %s)" % (self.name, self.publication)
