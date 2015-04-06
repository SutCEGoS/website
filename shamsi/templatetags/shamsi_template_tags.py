#coding=utf-8
__docformat__ = 'reStructuredText'
import datetime

from django.template import Library

from ..date.shamsi_date import Shamsi, convert_to_shamsi

register = Library()


@register.filter
def pdate(value, date_format=None):
    return convert_to_shamsi(value, date_format)


@register.filter
def pdatetime(value):
    u"""
    show persian date and time.
    example: 1 تير 1391 17:41:45
    :type value: datetime.datetime or datetime.date
    """
    return Shamsi(value).strfshamsi(Shamsi.LONG_DATETIME)


@register.filter
def pdatetime_long(value):
    u"""
    show persian date and time.
    example: 5 تير 1391 ساعت 14:0:0
    :type value: datetime.datetime
    """
    if not value:
        return '-'
    return Shamsi(value).strfshamsi(Shamsi.FULL_DATETIME_SEC)


@register.filter
def pdate_weekday(value):
    u"""
    example: پنجشنبه 1 تير 1391

    :type value:datetime.date
    """
    if not value:
        return '-'
    return Shamsi(value).strfshamsi(Shamsi.FULL_DATE)


@register.simple_tag
def pdate_weekday_today():
    u"""
    represent today persian datetime.
    example: پنجشنبه 1 تير 1391
    """
    return pdate_weekday(datetime.datetime.now())
