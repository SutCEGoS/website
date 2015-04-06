# -*- coding: utf-8 -*-
from django.db import models
from django.core import validators


class FarsiDate(models.CharField):
    description = 'A date in format 880323'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super(FarsiDate, self).__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(regex=r'\d\d\d\d\d\d'))


class FarsiTime(models.CharField):
    description = 'A time in format 2305'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 4
        super(FarsiTime, self).__init__(*args, **kwargs)


class FarsiDateTime(models.CharField):
    description = 'A datetime in format 8803231206'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(FarsiDateTime, self).__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(regex=r'\d\d\d\d\d\d\d\d\d\d'))

        #TODO enable custom output formatting
