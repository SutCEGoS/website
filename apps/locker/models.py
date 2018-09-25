from django.db import models
from model_utils import Choices
from apps.base.models import Member



# Create your models here.
class rack(models.Model):
        number = models.CharField(max_length=2)

        condition = {
                    'A':True,
                    'B':True,
                    'C':True,
                    'D':True,
                    'E':True,
                    'F':True,
                    'G':True,
                    'H':True,
                    'I':True,
                    'J':True,
                    'K':True,
                    'L':True,
                    'M':True,
                    'N':True,
                    'O':True,
                    'P':True,
                    }
        #date
        def __str__(self):
            return self.number
        def being_unable(self,X):
            self.condition[str(X)] = False
            return
        def get_condition(self,X):
            return self.condition[str(X)]


class locker(models.Model):
    charID = models.CharField(max_length=1)
    rack1 = models.ForeignKey(rack,null=True,related_name='1+')
    rack2 = models.ForeignKey(rack,null=True,related_name='2+')
    rack3 = models.ForeignKey(rack,null=True,related_name='3+')
    rack4 = models.ForeignKey(rack,null=True,related_name='4+')
    rack5 = models.ForeignKey(rack,null=True,related_name='5+')
    rack6 = models.ForeignKey(rack,null=True,related_name='6+')
    rack7 = models.ForeignKey(rack,null=True,related_name='7+')
    rack8 = models.ForeignKey(rack,null=True,related_name='8+')
    rack9 = models.ForeignKey(rack,null=True,related_name='9+')
    #
    recivers = {
                '11':None,
                '12':None,
                '13':None,
                '21':None,
                '22':None,
                '23':None,
                '31':None,
                '32':None,
                '33':None,
                }
    def __str__(self):
        return self.charID
