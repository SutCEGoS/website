# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils.safestring import mark_safe

from .date.shamsi_date import Shamsi


class ShamsiWidget(forms.DateInput):
    def render(self, name, value, attrs=None):
        input = super(ShamsiWidget, self).render(name, self.get_persian_value(value), attrs)
        output = '<div class="dateinput">' + input + '</div>'
        return mark_safe(output)

    def get_persian_value(self, value):
        if isinstance(value, datetime.datetime):
            date = value.date()
        elif isinstance(value, datetime.date):
            date = value
        else:
            return value
        output = Shamsi(date).strfshamsi(Shamsi.SHORT_DATE)
        return output


class SliderTimeWidget(forms.TimeInput):
    """
    یک ویجت برای زمان است که زمان را با یک ویجت لغزنده تغییر میدهد.

    """

    def render(self, name, value, attrs=None):
        input = super(SliderTimeWidget, self).render(name, self.get_time_value(value), attrs)
        output = '<div class="timeinput">' + input + '</div>'
        return mark_safe(output)

    def get_time_value(self, value):
        if isinstance(value, datetime.datetime):
            time = value.time()
        else:
            time = value
        return time


class ShamsiAdminSplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    یک ویجت است که تاریخ آن شمسی است و زمان آن به سبک زمان در قسمت ادمین است

    """

    def __init__(self, attrs=None):
        widgets = [ShamsiWidget, AdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)


class ShamsiSliderDateTimeWidget(forms.SplitDateTimeWidget):
    """
    یک ویجت است که تاریخ آن شمسی است و زمان آن به صورت لغزنده است.

    """

    def __init__(self, attrs=None):
        widgets = [ShamsiWidget, SliderTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)
