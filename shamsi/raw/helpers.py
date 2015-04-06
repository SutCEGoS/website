# coding=utf-8
'''
Created on Jan 15, 2011

@author: amirali
'''

from array import array
from datetime import datetime


def ensure_length(x, l):
    s = str(x)
    while (len(s) < l):
        s = '0' + s
    return s


def to_farsi(gy1, gm1, gd1):
    g_days_in_month = array('i', [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    j_days_in_month = array('i', [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29])
    gy = gy1 - 1600
    gm = gm1 - 1
    gd = gd1 - 1
    g_day_no = 365 * gy + (gy + 3) / 4 - (gy + 99) / 100 + (gy + 399) / 400
    for i in range(gm):
        g_day_no += g_days_in_month[i]
    if (gm > 1 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0))):
        g_day_no += 1
    g_day_no += gd
    j_day_no = g_day_no - 79
    j_np = j_day_no / 12053
    j_day_no = j_day_no % 12053
    jy = 979 + 33 * j_np + 4 * (j_day_no / 1461)
    j_day_no %= 1461
    if (j_day_no >= 366):
        jy += (j_day_no - 1) / 365
        j_day_no = (j_day_no - 1) % 365
    i = 0
    while True:
        if (j_day_no < j_days_in_month[i]):
            break
        i += 1
        j_day_no -= j_days_in_month[i]
    jm = i + 1
    jd = j_day_no + 1
    return '{0}{1}{2}'.format(ensure_length(jy % 100, 2), ensure_length(jm, 2), ensure_length(jd, 2))


def farsi_date_now():
    t = datetime.now()
    return to_farsi(t.year, t.month, t.day)


def farsi_time_now():
    t = datetime.now()
    return '{0}{1}'.format(ensure_length(t.hour, 2), ensure_length(t.minute, 2))


def farsi_datetime_now():
    return farsi_date_now() + farsi_time_now()


def farsi_date_format(date):
    return "{0}/{1}/{2}".format(date[0:2], date[2:4], date[4:6])


def farsi_datetime_format(date):
    return "{0}/{1}/{2} ساعت {3}:{4}".format(date[0:2], date[2:4], date[4:6], date[6:8], date[8:10])


def create_date_query(a, field):
    if a['type'] == "Y":
        return {field + '__gte': a['year'] + '0101', field + '__lte': a['year'] + '1230'}
    elif a['type'] == "M":
        return {field + '__gte': a['year'] + ensure_length(a['month'], 2) + '01',
                field + '__lte': a['year'] + ensure_length(a['month'], 2) + '31'}
    elif a['type'] == "D":
        return {field + '__exact': a['year'] + ensure_length(a['month'], 2) + ensure_length(a['day'], 2)}
    elif a['type'] == "W": #FIXME Week is approximate
        return {field + '__gte': a['year'] + ensure_length(a['month'], 2) + ensure_length((a['week'] - 1) * 7, 2),
                field + '__lt': a['year'] + ensure_length(a['month'], 2) + ensure_length(a['week'] * 7, 2)}
    return {}


def create_time_query(a, field): #TODO write me
    return {}


def create_datetime_query(a, field): #TODO write me
    return {}


def get_date_display(a):
    return u""


def is_interval_active2(start, finish):
    now = datetime.now()
    return (start <= now) and (now <= finish)


def is_interval_active(start, finish):
    now = datetime.now()
    temp = (start <= now) and (now <= finish)
    return temp


def is_interval_started(start):
    now = datetime.now()
    return start <= now 
    

