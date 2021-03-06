import datetime

from django.db import models
from tinymce.models import HTMLField

from apps.base.models import Named, Logged, Member

# from south.modelsinspector import add_introspection_rules
# add_introspection_rules([], ["^tinymce\.models.\HTMLField"])


class Poll(Named):
    start = models.DateTimeField(null=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    question = models.TextField()
    end = models.DateTimeField(null=True)
    details = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.question

    @property
    def active(self):
        if self.end:
            return datetime.datetime.now() < self.end.replace(tzinfo=None)
        return self.is_active

    def get_end(self):
        return str(self.end.replace(tzinfo=None))


class PollChoice(Named):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_result(self):
        a = Vote.objects.filter(choice=self).count()
        b = Vote.objects.filter(choice__in=PollChoice.objects.filter(poll=self.poll)).count()
        try:
            result = int((float(a) / float(b)) * 100)
        except:
            result = 0
        return result

    def get_count(self):
        return Vote.objects.filter(choice=self).count()


class Vote(Logged):
    member = models.ForeignKey(Member, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=63, null=True, blank=True)
    choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(verbose_name='user\'s IP', null=True, blank=True)



    class Meta:
        unique_together = ('member', 'choice')

    def __str__(self):
        return str(self.choice)

    def get_member(self):
        return self.member or self.username
