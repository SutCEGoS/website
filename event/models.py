import datetime

from django.db import models

from base.models import Named, Member, Logged


class Event(Named):
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    location = models.CharField(max_length=1023)
    reg_end = models.DateTimeField()
    image = models.ImageField(blank=True, null=True, upload_to='events')
    has_donate = models.BooleanField(default=False)
    has_register = models.BooleanField(default=True)

    @property
    def active(self):
        return datetime.datetime.now() < self.reg_end.replace(tzinfo=None)

    def get_end(self):
        return unicode(self.reg_end.replace(tzinfo=None))

    def get_count(self):
        return EventRegister.objects.filter(event=self).count()

    def registered(self, std_id):
        return EventRegister.objects.filter(event=self, std_id=std_id).exists()


class EventRegister(models.Model):
    std_id = models.CharField(max_length=63)
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.std_id

    def get_member(self):
        try:
            return Member.objects.get(std_id=self.std_id).username
        except Member.DoesNotExist:
            return "(invalid)"


class Donate(models.Model):
    name = models.CharField(max_length=63, null=True, blank=True)
    event = models.ForeignKey(Event)
    user = models.ForeignKey(Member, blank=True, null=True)
    value = models.IntegerField(default=0)
    is_success = models.NullBooleanField(null=True, default=True)

    def get_code(self):
        return "%s%s" % ("SHG", str(self.id))
