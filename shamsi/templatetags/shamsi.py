# -*- coding:utf-8 -*-
import datetime

from django import template

from ..date.shamsi_date import Shamsi, format_relative_date, convert_to_shamsi


register = template.Library()


@register.filter
def relative(date):
    return format_relative_date(date)


@register.filter
def to_shamsi(value):
    return convert_to_shamsi(value)
