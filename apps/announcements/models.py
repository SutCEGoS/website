from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel
from tinymce import models as tinymce_models

from apps.base.models import Member


class Announcement(TimeStampedModel):
    title = models.CharField(max_length=200)
    body = tinymce_models.HTMLField()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        if self.pk:
            return reverse('show-announcement', args=[self.pk])

    def register_view(self, user):
        if not user.is_authenticated():
            user = None

        return AnnouncementView.objects.create(
            user=user,
            announcement=self
        )

    @property
    def views(self):
        return self.announcementview_set.count()

    class Meta:
        ordering = ['-created']


class AnnouncementView(TimeStampedModel):
    user = models.ForeignKey(Member, null=True)
    announcement = models.ForeignKey(Announcement, null=False, blank=False)

    def __str__(self):
        return 'بازدید کاربر %s از %s' % (self.user.get_full_name(), self.announcement.title)
