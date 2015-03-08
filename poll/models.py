from django.db import models
from base.models import Named, Logged, Member


class Poll(Named):
    is_active = models.BooleanField(default=True)
    question = models.TextField()

    def __unicode__(self):
        return self.question

    @classmethod
    def get_active_poll(cls, site_type):
        return cls.objects.filter(site_type=site_type, is_active=True).last()


class PollChoice(Named):
    poll = models.ForeignKey(Poll)

    def __unicode__(self):
        return self.name

    def get_result(self):
        a = Vote.objects.filter(choice=self).count()
        b = Vote.objects.filter(choice__in=PollChoice.objects.filter(poll=self.poll)).count()
        try:
            result = int((float(a) / float(b))*100)
        except:
            result = 0
        return result


class Vote(Logged):
    member = models.ForeignKey(Member, null=True)
    choice = models.ForeignKey(PollChoice)

    def __unicode__(self):
        return unicode(self.choice)

