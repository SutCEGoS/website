import datetime

from django.db import models

from base.models import Named


class Event(Named):
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    location = models.CharField(max_length=1023)
    reg_end = models.DateTimeField()
    image = models.ImageField(blank=True, null=True, upload_to='events')

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
