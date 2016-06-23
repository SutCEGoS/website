# -*- coding: utf-8 -*-
import re
from datetime import date, datetime, timedelta, time
from _strptime import TimeRE

from django.utils import timezone
from .calverter import Calverter


MIN_YEAR = 1
MAX_YEAR = 1500


class Shamsi(object):
    SHAMSI_WEEKDAYS = (u"یکشنبه", u"دوشنبه", u"سه‌شنبه", u"چهارشنبه", u"پنجشنبه", u"جمعه", u"شنبه")
    SHAMSI_MONTHS = (
        u"فروردین", u"اردیبهشت", u"خرداد", u"تير", u"مرداد", u"شهریور", u"مهر", u"آبان", u"آذر", u"دی", u"بهمن",
        u"اسفند")
    letter_funcs = {'%A': lambda self: self.get_weekday_name(), '%B': lambda self: self.get_month_name(),
                    '%d': lambda self: self.exp(self.day), '%H': lambda self: self.exp(self.hour),
                    '%I': lambda self: self.exp(self.hour % 12), '%j': lambda self: self.exp(self.get_day_of_year(), 3),
                    '%m': lambda self: self.exp(self.month), '%M': lambda self: self.exp(self.minute),
                    '%p': lambda self: self.am_pm(), '%S': lambda self: self.exp(self.second),
                    '%U': lambda self: self.exp(self.get_week_number()), '%y': lambda self: self.exp(self.year)[2:],
                    '%Y': lambda self: self.exp(self.year), '%D': lambda self: self.day.__str__()}

    SHORT_DATE = '%Y-%m-%d'                             # '1392-03-27'
    COMMON_DATE = '%Y/%m/%d'                            # '1392/03/27'
    LONG_DATE = '%D %B %Y'                              # '27 خرداد 1392'
    FULL_DATE = '%A %D %B %Y'                           # 'دوشنبه 27 خرداد 1392'
    SHORT_DATETIME = '%Y-%m-%d %H:%M'                   # '1392-03-27 11:43'
    COMMON_DATETIME = '%Y/%m/%d %H:%M'                  # '1392/03/27 14:37'
    COMMON_DATETIME_SEC = '%Y/%m/%d %H:%M:%S'            # '1392/03/27 14:37:10'
    LONG_DATETIME = '%D %B %Y %H:%M'                    # '27 خرداد 1392 14:37'
    LONG_DATETIME_SEC = '%D %B %Y %H:%M:%S'             # 27 خرداد 1392 14:37:10
    FULL_DATETIME = u'%A %D %B %Y ساعت %H:%M'           # 'دوشنبه 27 خرداد 1392 ساعت 14:37'
    FULL_DATETIME_SEC = u'%A %D %B %Y ساعت %H:%M:%S'    # 'دوشنبه 27 خرداد 1392 ساعت 14:37:00'

    def __init__(self, pydate=None, year=None, month=None, day=None, hour=0, minute=0, second=0):
        """
            :type pydate: date or datetime
        """
        self.pydate = None
        self.jd = None
        self.year, self.month, self.day = None, None, None
        self.hour, self.minute, self.second = None, None, None
        if Shamsi.check_date_args(year, month, day):
            self.jd = Shamsi.get_julian_date(year, month, day, 'shamsi')
            Shamsi.check_time_args(hour, minute, second)
            for name, val in locals().iteritems():
                setattr(self, name, val)
        if pydate:
            if not isinstance(pydate, (datetime, date)):
                raise ValueError('the Shamsi pydate argument should be date or datetime')
            self.jd = Shamsi.get_julian_date(pydate.year, pydate.month, pydate.day)
            st = pydate.timetuple()
            self.year, self.month, self.day = self.get_jalali()
            self.hour, self.minute, self.second = st.tm_hour, st.tm_min, st.tm_sec
        self.__set_pydate(pydate)

    def __repr__(self):
        return 'Shamsi' + str((self.year, self.month, self.day, self.hour, self.minute, self.second))

    def is_none(self):
        return self.pydate is None and self.jd is None and self.year is None

    def __set_pydate(self, pydate):
        if type(pydate) is date:
            # noinspection PyTypeChecker
            self.pydate = datetime.combine(pydate, time.min)
        elif type(pydate) is datetime:
            self.pydate = pydate
        else:
            self.pydate = self.get_pydate()

    def strfshamsi(self, pattern):
        """
        یک تاریخ از نوع شمسی را به صورت رشته‌ای با الگوی داده شده در می‌آورد
        الگوی داده شده شبیه
        strftime
        است. الگوهای معمول تاریخ شمسی نیز به صورت متغیرهای کلاس، آورده شده‌اند.

        :param str or unicode pattern: date string format like '%Y-%m-%d'
        :rtype

        example:
        >>> n=datetime.now()
        >>> n
        datetime.datetime(2013, 6, 17, 14, 37, 59, 597000)
        >>> shamsi=Shamsi(n)
        >>> shamsi
        Shamsi(1392, 3, 27, 14, 37, 59)
        >>> shamsi.strfshamsi(Shamsi.SHORT_DATE)
        u'1392-03-27'
        >>> shamsi.strfshamsi(Shamsi.COMMON_DATE)
        u'1392/03/27'
        >>> print shamsi.strfshamsi(Shamsi.LONG_DATE)
        27 خرداد 1392
        >>> print shamsi.strfshamsi(Shamsi.FULL_DATE)
        دوشنبه 27 خرداد 1392

        >>> shamsi.strfshamsi(Shamsi.SHORT_DATETIME)
        u'1392-03-27 14:37'
        >>> shamsi.strfshamsi(Shamsi.COMMON_DATETIME)
        u'1392/03/27 14:37'
        >>> print shamsi.strfshamsi(Shamsi.LONG_DATETIME)
        27 خرداد 1392 14:37
        >>> print shamsi.strfshamsi(Shamsi.FULL_DATETIME)
        دوشنبه 27 خرداد 1392 ساعت 14:37
        >>> print shamsi.strfshamsi(Shamsi.FULL_DATETIME_SEC)
        دوشنبه 27 خرداد 1392 ساعت 14:37:59

        >>> shamsi.strfshamsi('%Y')
        u'1392'
        >>> print shamsi.strfshamsi('%p')
        بعد از ظهر
        >>> shamsi.strfshamsi('%y/%m/%d')
        u'92/03/27'
        >>> print shamsi.strfshamsi(u'%A %d %B %Y ساعت %H:%M %p')
دوشنبه 27 خرداد 1392 ساعت 14:37 بعد از ظهر
        """
        if self.is_none():
            return u'ندارد'
        letter_re = re.compile(r'%[a-z A-Z]', re.UNICODE)
        return letter_re.sub(lambda m: Shamsi.letter_funcs[m.group(0)](self), pattern)

    @classmethod
    def pstr_shamstr(cls, pydate_string, py_pattern=SHORT_DATE, shamsi_pattern=SHORT_DATE):
        """
        convert python date string to Shamsi string
        :param cls:
        :param str pydate_string: python date string like '2013-06-17'
        :param str py_pattern: python string  format like '%Y-%m-%d'
        :param str shamsi_pattern: strftime format like '%Y-%m-%d'.for common format look Shamsi const like cls.SHORT_DATE
        :rtype unicode
        examples:
        >>> print Shamsi.pstr_shamstr('2013-06-17',Shamsi.SHORT_DATE, Shamsi.LONG_DATE)
27 خرداد 1392

equal to:
        >>> print Shamsi.pstr_shamstr('2013-06-17','%Y-%m-%d', '%d %B %Y')
        27 خرداد 1392
        >>> print Shamsi.pstr_shamstr('2013-06-17 14:37',Shamsi.SHORT_DATETIME, Shamsi.FULL_DATE)
        دوشنبه 27 خرداد 1392
        >>> print Shamsi.pstr_shamstr('2013-06-17 14:37',Shamsi.SHORT_DATETIME, Shamsi.COMMON_DATE)
1392/03/27
        >>> print Shamsi.pstr_shamstr('2013-06-17 14:37',Shamsi.SHORT_DATETIME, Shamsi.SHORT_DATETIME)
        1392-03-27 14:37
        >>> Shamsi.pstr_shamstr('2013 June 17', '%Y %B %d', Shamsi.COMMON_DATE)
        u'1392/03/27'

        """
        d = datetime.strptime(pydate_string, py_pattern)
        return cls(d).strfshamsi(shamsi_pattern)

    @classmethod
    def str_to_shamsi(cls, data_string, date_format):
        u"""
        یک رشته‌ی شمسی را میگیرد و الگوی آن را می‌گیرد و کلاس
        Shamsi
        آن را برمی‌گرداند.
        :param str data_string: data_string. e.g. '1392-3-27'
        :param str date_format: date_format. e.g. '%Y-%m-%d %H:%M:%S'
        :rtype: Shamsi


        >>> Shamsi.str_to_shamsi('1392-3-27',Shamsi.SHORT_DATE )
        Shamsi(1392, 3, 27, 0, 0, 0)
        >>> Shamsi.str_to_shamsi('1392-3-27 14:37',Shamsi.SHORT_DATETIME )
        Shamsi(1392, 3, 27, 14, 37, 0)
        >>> Shamsi.str_to_shamsi('1392-3-27 14:37:10','%Y-%m-%d %H:%M:%S' )
        Shamsi(1392, 3, 27, 14, 37, 10)
        >>> Shamsi.str_to_shamsi('1392/3/27',Shamsi.COMMON_DATE )
        Shamsi(1392, 3, 27, 0, 0, 0)
        >>> Shamsi.str_to_shamsi(u'27 خرداد 1392',Shamsi.LONG_DATE)
        Shamsi(1392, 3, 27, 0, 0, 0)

        """
        tmp = TimeRE()
        tmp.update(
            {'A': tmp._TimeRE__seqToRE(cls.SHAMSI_WEEKDAYS, 'A'), 'B': tmp._TimeRE__seqToRE(Shamsi.SHAMSI_MONTHS, 'B')})

        _TimeRE_cache = tmp
        _regex_cache = {}
        hour = minute = second = 0
        year = 1900
        month = day = 1
        format_regex = _regex_cache.get(date_format)
        if not format_regex:
            try:
                format_regex = _TimeRE_cache.compile(date_format)
            except KeyError as err:
                bad_directive = err.args[0]
                if bad_directive == "\\":
                    bad_directive = "%"
                del err
                raise ValueError("'%s' is a bad directive in date_format '%s'" %
                                 (bad_directive, date_format))
            # IndexError only occurs when the date_format string is "%"
            except IndexError:
                raise ValueError("stray %% in date_format '%s'" % date_format)
        found = format_regex.match(data_string)
        if not found:
            raise ValueError("time data %r does not match date_format %r" %
                             (data_string, date_format))
        if len(data_string) != found.end():
            raise ValueError("unconverted data remains: %s" %
                             data_string[found.end():])
        found_dict = found.groupdict()
        for group_key in found_dict.iterkeys():
            if group_key == 'y':
                year = int(found_dict['y'])
            elif group_key == 'j':
                d = int(found_dict['j'])
                if d <= 186:
                    month = int(d / 31) + 1
                    day = d % 31
                elif 186 < d < 367:
                    nd = d - 186
                    if d == 366:
                        month = 12
                        day = 30
                    else:
                        month = int(nd / 30) + 7
                        day = nd % 30
                else:
                    raise ValueError('It is invalid value for day')
            elif group_key == 'Y':
                year = int(found_dict['Y'])
            elif group_key == 'm':
                month = int(found_dict['m'])
            elif group_key == 'd':
                day = int(found_dict['d'])
            elif group_key == 'H':
                hour = int(found_dict['H'])
            elif group_key == 'M':
                minute = int(found_dict['M'])
            elif group_key == 'S':
                second = int(found_dict['S'])
            elif group_key == 'B':
                month = cls.SHAMSI_MONTHS.index(found_dict['B']) + 1
            elif group_key == 'A':
                weekday = cls.SHAMSI_WEEKDAYS.index(found_dict['A'])
        return cls(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def get_month_name(self):
        if self.is_none():
            return u'ندارد'
        return Shamsi.SHAMSI_MONTHS[self.month - 1]

    @classmethod
    def check_date_args(cls, year, month, day):
        """
بررسی معتبر بودن آرگومان‌‌های تاریخ

        """
        l = [year, month, day]
        if all(a is None for a in l):
            return False
        if any(a is None for a in l):
            raise ValueError(u'Shamsi arguments are invalid')
        if not year in range(MIN_YEAR, MAX_YEAR):
            raise ValueError(u'year is invalid number')
        if not month in range(1, 13):
            raise ValueError(u'month must be in 1..12')
        if month < 7 and not day in range(1, 32):
            raise ValueError(u'day must be in 1..31')
        if month == 12 and day == 30:
            if not cls.leap_year(year):
                raise ValueError(u'year is not leap so day must be in 1..29')
        if month > 6 and not day in range(1, 31):
            raise ValueError(u'day must be in 1..30')
        return True

    @classmethod
    def check_time_args(cls, hour, minute, second):
        u"""
        بررسی معتبر بودن آرگومان‌‌های زمان

        """
        if not hour in range(0, 24):
            raise ValueError(u'hour must be in 0..23')
        if not minute in range(0, 60):
            raise ValueError(u'minute must be in 0..59')
        if not second in range(0, 60):
            raise ValueError(u'second must be in 0..59')
        return True

    @classmethod
    def get_julian_date(cls, year, month, day, tp='miladi'):
        """
        get julian date from gregorian date or jalali date
        example:
        >>> Shamsi.get_julian_date(1392,4,1,'shamsi')
        2456465.5
        >>> Shamsi.get_julian_date(2013,6,22)
        2456465.5

        """
        cal = Calverter()
        if tp == 'miladi':
            return cal.gregorian_to_jd(year, month, day)
        return cal.jalali_to_jd(year, month, day)

    def get_jalali(self):
        u"""
        سه عدد برمی‌گرداند که معرف تاریخ شمسی است

        """
        cal = Calverter()
        jalali = cal.jd_to_jalali(self.jd)
        return jalali

    def get_pydate(self):
        u"""
        :rtype datetime
        :return:
        """
        if not self.jd:
            return None
        cal = Calverter()
        y, m, d = cal.jd_to_gregorian(self.jd)
        return datetime(y, m, d, self.hour, self.minute, self.second)

    def get_weekday_name(self):
        u"""
        example:
        >>> print Shamsi(datetime.now()).get_weekday_name()
شنبه
        """
        cal = Calverter()
        return Shamsi.SHAMSI_WEEKDAYS[cal.jwday(self.jd)]

    def is_leap(self):
        u"""
        آیا سال کبیسه است
        """
        return Shamsi.leap_year(self.year)

    @classmethod
    def leap_year(cls, year):
        u"""
    سال را گرفته مشخص می‌کند که کبیسه است یا نه.
        :type year: int
        :rtype:bool
        """
        cal = Calverter()
        return cal.leap_jalali(year)

    def get_iso_day(self):
        cal = Calverter()
        return cal.jd_to_iso_day(self.jd)

    def get_day_of_year(self):
        u"""
        چندمین روز سال است
        :rtype:int
        """
        m = self.month
        d = self.day
        if m < 6:
            return (m - 1) * 31 + d
        return 6 * 31 + (m - 7) * 30 + d

    def am_pm(self):
        if self.hour > 11:
            return u'بعد از ظهر'
        return u'قبل از ظهر'

    def get_week_number(self):
        u"""
        در هفته‌ی چندم قرار دارد.
        توجه:
        روزهای قبل از اولین شنبه‌ی سال، در هفته‌ی 0 در نظر گرفته می‌شوند.

        :return: week number
        """
        cal = Calverter()
        jd = Shamsi(year=self.year, month=1, day=8).jd
        f_saturday = cal.weekday_before(6, jd)
        if self.jd < f_saturday:
            return 0
        week_number = int((self.jd - f_saturday) / 7)
        return week_number + 1

    def get_julian_weekday(self, shamsi_week_day, first_day='sunday'):
        """
        با توجه به روز هفته‌ی شمسی که در آن شنبه، صفر در نظر گرفته شده، معادل روز هفته را در تاریخ میلادی که معمولا یکشنبه را
        به عنوان روز اول در نظر میگرند، برمی‌گرداند
        :param int shamsi_week_day: shamsi weekday as a decimal number 0(Saturday)..6
        :param str first_day: julian first day. generally sunday is first day.
        :return:
        """
        if first_day == 'sunday':
            return (6, 0, 1, 2, 3, 4, 5)[shamsi_week_day]
        if first_day == 'monday':
            return (5, 6, 0, 1, 2, 3, 4)[shamsi_week_day]

    def week_day_before(self, shamsi_week_day):
        u"""
        تاریخ شمسی را برای روزهای گذشته برمی‌گرداند.
        یعنی اگر مثلا امروز دوشنبه 21 مرداد 91 باشد
        week_day_before(0)
        روز شنبه که معادل تاریخ
        Shamsi(year=1392, month=5, day=19)
        را میدهد
        week_day_before(1)
        یکشنبه که معادل تاریخ
        Shamsi(year=1392, month=5, day=20)
        را میدهد
       week_day_before(2)
        همان دوشنبه 21 مرداد 91 را میدهد
       week_day_before(3)
        روز سه شنبه که معادل تاریخ
        Shamsi(year=1392, month=5, day=15)
        را میدهد
        >>> shamsi = Shamsi(year=1392, month=5, day=21)
        >>> shamsi.week_day_before(4)
        Shamsi(1392, 5, 16, 0, 0, 0)

        :param int shamsi_week_day: weekday as a decimal number 0(Saturday)..6
        :rtype: Shamsi
        """
        cal = Calverter()
        jd = cal.weekday_before(self.get_julian_weekday(shamsi_week_day), self.jd)
        jal = cal.jd_to_jalali(jd)
        return Shamsi(year=jal[0], month=jal[1], day=jal[2])

    def search_weekday(self, shamsi_weekday, direction, offset):
        cal = Calverter()
        jd = cal.search_weekday(self.get_julian_weekday(shamsi_weekday), self.jd, direction, offset)
        jal = cal.jd_to_jalali(jd)
        return Shamsi(year=jal[0], month=jal[1], day=jal[2])

    @classmethod
    def jd_to_shamsi(cls, jd):
        cal = Calverter()
        jal = cal.jd_to_jalali(jd)
        return cls(year=jal[0], month=jal[1], day=jal[2])

    def get_python_week_day_before(self, week_day):
        """
        :param week_day: weekday as a decimal number 0(Sunday)..6
        :return:
        """
        cal = Calverter()
        jd = cal.weekday_before(week_day, self.jd)
        jal = cal.jd_to_gregorian(jd)
        return datetime(year=jal[0], month=jal[1], day=jal[2])

    def get_day_of_shamsi_month(self, offset=1):
        """
        روز
        offset
        ام از ماه شمسی را می‌دهد

        >>> dt = datetime(2013, 9, 4)
        >>> shamsi=Shamsi(dt.date())
        >>> shamsi
        Shamsi(1392, 6, 13, 0, 0, 0)
        >>> shamsi.get_day_of_shamsi_year(10)
        datetime.datetime(2013, 9, 1, 0, 0)
        درواقع در مثال بالا می‌خواهیم بدانیم که روز 10ام از ماه شهریور سال 92 معادل چه تاریخ میلادی است

        :param int offset: offset of month
        :rtype:datetime
        """
        d = self.pydate - timedelta(self.day - offset)
        return datetime.combine(d, time.min)

    def get_day_of_shamsi_year(self, offset=1):
        u"""
    روز
    offset
    ام از سال شمسی را به تاریخ میلادی برمی‌گرداند.
    e.g
        >>> shamsi = Shamsi(datetime(2013, 9, 4))
        >>> shamsi.get_day_of_shamsi_year(100)
        datetime.datetime(2013, 6, 28, 0, 0)
    درواقع در مثال بالا ابتدا یک تاریخ شمسی ایجاد کرده‌ایم که معادل تاریخ داده شده است
     وبعد می‌خواهیم بدانیم که 100 امین روز از سال شمسی تاریخ شمسی بدست آمده، معادل چه تاریخ میلادی است

        """
        d = '%s-%s' % (self.year, offset)
        return Shamsi.str_to_shamsi(d, '%Y-%j').pydate

    def exp(self, num, zf=2):
        """
        convert 1 to '01'
        example:
        >>> Shamsi().exp(1)
        u'01'
        >>> Shamsi().exp(1,3)
        u'001'
        :param num: number
        :param zf:
        :return:
        """
        return unicode(num).zfill(zf)

    def __eq__(self, other):
        return (self.year, self.month, self.day, self.hour, self.minute, self.second, self.jd) == (
            other.year, other.month, other.day, other.hour, other.minute, other.second, other.jd)


def format_relative_date(d):
    #TODO: convert to farsi date
    #TODO: rewrite with more care
    now = timezone.now()
    diff = now - d
    year = d.strftime('%y')
    days_dic = {'Sunday': u'یکشنبه', 'Monday': u'دوشنبه', 'Tuesday': u'سه شنبه', 'Wednesday': u'چهارشنبه',
                'Thursday': u'پنجشنبه', 'Friday': u'جمعه', 'Saturday': u'شنبه'}
    day_of_week = days_dic[d.strftime('%A')]
    date = convert_to_shamsi(d.date())
    time = d.strftime('%H:%M')

    if year == now.strftime('%y'):
        if diff.days < 7:
            if diff.days < 1:
                if diff.seconds < 60:
                    a = u'چند لحظه قبل'
                else:
                    a = time
            else:
                a = u'{0} ساعت {1}'.format(day_of_week, time)
        else:
            a = date + day_of_week
    else:
        a = date + day_of_week
    return a


def convert_to_shamsi(value, date_format=None):
    u"""
    example : 1 تير 1391 if value type is datetime.date
    example : 5 تير 1391 ساعت 14:0:0 if value type is datetime.datetime with time
    example : 1 تير 1391 if value type is datetime.datetime with time(0,0)
    :type value:datetime.date or datetime.datetime
    :rtype: unicode
    """
    if not value:
        return u'-'
    if date_format is None:
        if type(value) is date:
            date_format = Shamsi.LONG_DATE
        if type(value) is datetime:
            if value.time() == time(0, 0):
                return Shamsi(value).strfshamsi(Shamsi.LONG_DATE)
            else:
                date_format = Shamsi.LONG_DATETIME
    return Shamsi(value).strfshamsi(date_format)
