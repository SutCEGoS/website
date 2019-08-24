from django.db.models import *


class Book(Model):
    name = CharField(verbose_name="نام", max_length=100)
    author = CharField(verbose_name="نویسنده", max_length=100, null=True, blank=True)
    translator = CharField(verbose_name="مترجم", max_length=100, null=True, blank=True)
    publication = CharField(verbose_name="ناشر", max_length=100, null=True, blank=True)
    image = ImageField(verbose_name="تصویر کتاب")
    count = IntegerField(verbose_name="تعداد", default=1)


    def __str__(self):
        return "%s(انتشارات %s)" % (self.name, self.publication)

    def get_image_tag(self):
        pass

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"
