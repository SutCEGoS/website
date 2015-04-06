# -*- coding: utf-8 -*-
__docformat__ = 'reStructuredText'
import datetime

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from .widgets import ShamsiWidget, ShamsiAdminSplitDateTimeWidget, ShamsiSliderDateTimeWidget
from .date.shamsi_date import Shamsi


class ShamsiDateField(forms.DateField):
    widget = ShamsiWidget
    default_error_messages = {'invalid': u"یک تاریخ معتبر وارد نمایید."}

    def to_python(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        try:
            return Shamsi.str_to_shamsi(value, Shamsi.SHORT_DATE).get_pydate().date()
        except (ValueError, ValidationError):
            raise ValidationError(self.default_error_messages['invalid'])


class ShamsiAdminSplitDateTimeField(forms.MultiValueField):
    """
    a form field that its date is  ShamsiDateField and its time is
    TimeField and its widget is ShamsiAdminSplitDateTimeWidget.
    this field is suitable for admin
    """
    widget = ShamsiAdminSplitDateTimeWidget
    default_error_messages = {
        'invalid_date': u'یک تاریخ معتبر وارد نمایید.',
        'invalid_time': u'یک زمان معتبر وارد نمایید.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages
        localize = kwargs.get('localize', False)
        fields = (
            ShamsiDateField(error_messages={'invalid': errors['invalid_date']}, localize=localize),
            forms.TimeField(error_messages={'invalid': errors['invalid_time']}, localize=localize),
        )
        super(ShamsiAdminSplitDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_time'])
            return datetime.datetime.combine(*data_list)
        return None


class ShamsiDateTimeField(forms.MultiValueField):
    """
    a form field that its date is  ShamsiDateField and its time is
    TimeField and its widget is ShamsiSliderDateTimeWidget.

    """
    widget = ShamsiSliderDateTimeWidget
    default_error_messages = {
        'invalid_date': u'یک تاریخ معتبر وارد نمایید.',
        'invalid_time': u'یک زمان معتبر وارد نمایید.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages
        localize = kwargs.get('localize', False)
        fields = (
            ShamsiDateField(error_messages={'invalid': errors['invalid_date']}, localize=localize),
            forms.TimeField(error_messages={'invalid': errors['invalid_time']}, localize=localize),
        )
        super(ShamsiDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_time'])
            return datetime.datetime.combine(*data_list)
        return None

    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a Python
        datetime.datetime object.
            """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            value = datetime.datetime(value.year, value.month, value.day, 0, 0, 0)
            return value
        try:
            date_time = Shamsi.str_to_shamsi(value, Shamsi.SHORT_DATETIME).get_pydate()
            return date_time
        except (ValidationError, ValueError):
            raise ValidationError(self.default_error_messages['invalid_date'])
