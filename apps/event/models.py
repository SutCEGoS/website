import datetime

from django.db import models

from apps.base.models import Named, Member
from apps.event.normalize import unicode_normalize, replace_persian_numbers


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
        return str(self.reg_end.replace(tzinfo=None))

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
            x = unicode_normalize(self.std_id)
        except:
            try:
                x = replace_persian_numbers(self.std_id)
            except:
                x = self.std_id
        try:
            return Member.objects.get(std_id__contains=x).username
        except Member.DoesNotExist:
            return "(invalid)"
        except Member.MultipleObjectsReturned:
            return "(multiple!)"


class Donate(models.Model):
    name = models.CharField(max_length=63, null=True, blank=True)
    event = models.ForeignKey(Event)
    user = models.ForeignKey(Member, blank=True, null=True)
    value = models.IntegerField(default=0)
    is_success = models.NullBooleanField(null=True, default=True)

    def get_code(self):
        return "%s%s" % ("SHG", str(self.id))
