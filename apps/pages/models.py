from django.db import models
from apps.base.models import Logged, Member
from model_utils import Choices


class Link(models.Model):
    slug = models.SlugField(db_index=True, null=False, blank=False, verbose_name='آدرس در سایت')
    url = models.URLField(blank=False, null=False, verbose_name='آدرس لینک')
    title = models.CharField(max_length=90, verbose_name='عنوان')
    login_required = models.BooleanField(default=False, verbose_name='فقط افراد عضو')
    enabled = models.BooleanField(default=True, verbose_name='فعال')
    type = models.IntegerField(choices=Choices(
        (0, 'Frame', 'نمایش در سایت'),
        (1, 'Redirect', 'هدایت به آدرس')
    ), verbose_name='نحوهٔ نمایش')

    @property
    def visit_count(self):
        return self.visits.count()

    def visit(self, user):
        return LinkVisit.objects.create(
            link=self,
            member=user
        )


class LinkVisit(Logged):
    link = models.ForeignKey(Link, related_name='visits', blank=False, null=False, verbose_name='لینک', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, blank=True, null=True, verbose_name='کاربر', on_delete=models.CASCADE)

