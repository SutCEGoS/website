# -*- coding: utf-8 -*-
from django import template
from calverter import Calverter

from datetime import date
from string import split
import datetime

register = template.Library()

MONTHS = ("فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن", "اسفند")
cal = Calverter()


def convert_stringdate_to_pythondate(string):
    l1 = split(string, "-")
    year = int(l1[0])
    month = int(l1[1])
    day = int(l1[2])
    return date(year, month, day)


def pdate_string(value, forceTime=False):
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    jalali = cal.jd_to_jalali(jd)
    if forceTime:
        try:
            h = value.hour
            m = value.minute
            s = value.second
            return "%s/%s/%s %s:%s:%s" % (jalali[0], jalali[1], jalali[2], h, m, s)
        except:
            pass

    return str(jalali[0]) + "-" + expand_month_day(str(jalali[1])) + "-" + expand_month_day(str(jalali[2]))


def expand_month_day(value):
    if len(str(value)) == 1:
        result = "0%s" % value
        return result
    return value

#
#def pdate(value):
#    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
#    y, m, d = cal.jd_to_jalali(jd)
#    return date(year=y, month=m, day=d)


def get_current_month():
    now = datetime.datetime.today()
    year, month, day = pdate_seperate(now)
    return month


def get_current_day():
    now = datetime.datetime.today()
    year, month, day = pdate_seperate(now)
    return day


def get_current_year():
    now = datetime.datetime.today()
    year, month, day = pdate_seperate(now)
    return year


def pdate_seperate(value):
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_jalali(jd)
    return y, m, d


def pdate_time(value):
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_jalali(jd)
    return datetime.datetime(year=y, month=m, day=d, hour=value.hour, minute=value.minute, second=value.second)


def pdate_to_miladi(value):
    jd = cal.jalali_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_gregorian(jd)
    return date(year=y, month=m, day=d)


def pdate_string_to_miladi(year, month, day):
    jd = cal.jalali_to_jd(year, month, day)
    y, m, d = cal.jd_to_gregorian(jd)
    return date(year=y, month=m, day=d)


def jalili_to_miladi(year, month, day):
    jd = cal.jalali_to_jd(year, month, day)
    y, m, d = cal.jd_to_gregorian(jd)
    return date(year=y, month=m, day=d)

#def pdate_to_miladi(year,month,day):
#    jd = cal.jalali_to_jd(year, month, day)
#    y,m,d = cal.jd_to_gregorian(jd)
#    return date(year=y,month=m,day=d)

def pdate_persian_month(value):
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    jalali = cal.jd_to_jalali(jd)
    return str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(jalali[0])


@register.filter
def pdate_filter(value):
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    jalali = cal.jd_to_jalali(jd)
    return str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(jalali[0])


@register.filter
def pdate_long_filter(value):
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    jalali = cal.jd_to_jalali(jd)

    return cal.JALALI_WEEKDAYS[cal.jwday(jd)] + "، " + str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(
        jalali[0])


@register.simple_tag
def today_pdate_filter():
    return pdate_string(date.today())
    #jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    #jalali = cal.jd_to_jalali(jd)
    #return str(jalali[2]) + " " + MONTHS[jalali[1]-1] + " " + str(jalali[0])


def pdate2(value):
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    jalali = cal.jd_to_jalali(jd)
    return str(jalali[0]) + "/" + str(jalali[1]) + "/" + str(jalali[2])


def split_date(string):
    l1 = split(string, "-")
    year = int(l1[0])
    month = int(l1[1])
    day = int(l1[2])
    return year, month, day