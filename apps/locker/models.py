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

    BROKEN_LOCKERS = ['A42',
                      'B23', 'B41',
                      'D11',
                      'F42',
                      'G12', 'G22', 'G42', 'G43',
                      'H12',
                      'J12',
                      'K23', 'K32', 'K42',
                      'N22', 'N32', 'N41',
                      'O13',
                      'P13', 'P22', 'P23', 'P31',
                      'Q21',

                      # new lockers
                      'A21', 'A23',
                      'C21', 'C31', 'C33', 'C42', 'C43',
                      'D12', 'D13',
                      'E42', 'E22',
                      'G21', 'G43',
                      'H32', 'H42', 'H22',
                      'I21', 'I23', 'I31', 'I42',
                      'J22', 'J32',
                      'K43', 'K22', 'K11',
                      'L11', 'L12', 'L23', 'L33', 'L43',
                      'N12',
                      'O12', 'O22', 'O23', 'O31', 'O33', 'O32', 'O41',
                      'P12', 'P33',
                      'Q13',
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
            return 1  # BROKEN
        rack = Rack.objects.filter(name=rack_name, archived=False)
        if len(rack) != 0:
            return 2  # CHOSEN BEFORE
        if not re.fullmatch(r'[A-LN-Q][1-4][1-3]', rack_name):
            return 3  # NOT FOUND
        return 0  # READY
