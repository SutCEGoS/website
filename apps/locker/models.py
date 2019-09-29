from django.db import models
from model_utils import Choices
from apps.base.models import Member, Transaction
import re

class Rack(models.Model):
    CONDITION = Choices(
        (0, 'available'),
        (1, 'unavailable'),
        (2, 'is_paying')
    )

    BROKEN_LOCKERS = ['A42', 'B23', 'B41',
                      'D11',
                      'F42', 'G12', 'G22', 'G42', 'G43',
                      'H12', 'J12',
                      'K23',
                      'K32', 'K42',
                      'O13', 'N22',
                      'N32', 'N41', 'Q21',
                      'P13', 'P22', 'P23', 'P31',
                      ]

    name = models.CharField(max_length=3)
    receiver = models.ForeignKey(Member, blank=True, null=True, on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction, null=True, on_delete=models.SET_NULL)
    receivie_date = models.DateTimeField(auto_now_add=True)
    condition = models.PositiveSmallIntegerField(choices=CONDITION, default=0)
    archived = models.BooleanField(default=False, null=True, verbose_name="آرشیو شده")

    def __str__(self):
        return self.name

    @classmethod
    def get_rack_status(cls, rack_name):
        if rack_name in cls.BROKEN_LOCKERS:
            return 1    # BROKEN
        rack = Rack.objects.filter(name=rack_name, archived=False)
        if len(rack) != 0:
            return 2    # CHOSEN BEFORE
        if not re.fullmatch(r'[A-LN-P][1-4][1-3]', rack_name):
            return 3    # NOT FOUND
        return 0        # READY


class sell(models.Model):
    value = models.IntegerField(default=20000)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    locker = models.ForeignKey(Rack, on_delete=models.CASCADE)
    is_success = models.NullBooleanField(null=True, default=True)
    authority = models.CharField(max_length=63, null=True)

    def __str__(self):
        return "'  %s  ' HAS BEEN SOLD TO '  %s ( %s ) '" % (self.locker.name, self.user, self.user.std_id)
