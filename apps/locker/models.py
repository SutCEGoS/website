from django.db import models
from model_utils import Choices
from apps.base.models import Member



# Create your models here.
class rack(models.Model):
        CONDITION = Choices((0, 'available'),
                           (1, 'unavailable'),
                           )
        name = models.CharField(max_length=3)
        receiver = models.ForeignKey(Member,blank=True,null=True, on_delete=models.CASCADE)
        payment = models.BooleanField(default=False)
        receivie_date = models.DateTimeField(auto_now_add=True)
        condition = models.PositiveSmallIntegerField(choices=CONDITION,default=0)
        def __str__(self):
            return self.name
class sell(models.Model):
    value = models.IntegerField(default=20000)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    locker = models.ForeignKey(rack, on_delete=models.CASCADE)
    is_success = models.NullBooleanField(null=True, default=True)
    authority = models.CharField(max_length=63)
    tried = models.NullBooleanField(default=False)
    def __str__(self):
        return "'  %s  ' HAS BEEN SOLD TO '  %s ( %s ) '" %( self.locker.name , self.user , self.user.std_id)
