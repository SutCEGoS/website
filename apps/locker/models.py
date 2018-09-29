from django.db import models
from model_utils import Choices
from apps.base.models import Member



# Create your models here.
class rack(models.Model):
        CONDITION = Choices((0, 'available'),
                           (1, 'unavailable'),
                           )
        name = models.CharField(max_length=3)
        receiver = models.ForeignKey(Member,blank=True,null=True)
        condition = models.PositiveSmallIntegerField(choices=CONDITION,default=0)
        def __str__(self):
            return self.name
        def get_serialized(self, member):
            return {
                'data_id': self.id,
                'name': self.name,
                'condition_id': self.condition,
                'condition_name': self.get_condition_display(),
            }
