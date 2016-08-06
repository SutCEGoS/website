# -*- coding: utf-8 -*-
import datetime
from unittest import TestCase
from arsh.shamsi.templatetags.shamsi_template_tags import pdate
from date.shamsi_date import Shamsi
from .date.helpers import Interval


class HelpersTest(TestCase):
    def test_get_week_number(self):
        d = datetime.datetime(2013, 1, 1)
        self.assertEqual(Interval(d).get_week_number(), 0)
        d = datetime.datetime(2013, 1, 11)
        self.assertEqual(Interval(d).get_week_number(), 1)
        d = datetime.datetime(2013, 2, 2)
        self.assertEqual(Interval(d).get_week_number(), 4)
        d = datetime.datetime(2013, 2, 3)
        self.assertEqual(Interval(d).get_week_number(), 5)

    def test_get_week_interval(self):
        sat = datetime.datetime(2013, 8, 3)
        mon = datetime.datetime(2013, 8, 5, 15, 32)
        fri = datetime.datetime(2013, 8, 9)
        self.assertEqual(Interval(mon).get_week_interval(), (sat, mon))
        self.assertEqual(Interval(fri).get_week_interval(), (sat, fri))

    def test_now_interval(self):
        d2 = datetime.datetime(2013, 9, 4, 10, 47, 50)
        self.assertEqual((datetime.datetime(2013, 9, 4), d2), Interval(d2).now_interval())

    def test_day_interval(self):
        d2 = datetime.datetime(2013, 9, 4)
        # noinspection PyTypeChecker
        self.assertEqual((datetime.datetime(2013, 9, 4), datetime.datetime.combine(d2.date(), datetime.time.max)),
                         Interval(d2).day_interval())

    def test_month_interval(self):
        d2 = datetime.datetime(2013, 9, 4)
        self.assertEqual((datetime.datetime(2013, 8, 23), datetime.datetime(2013, 9, 4)),
                         Interval(d2).month_interval())


class ShamsiTest(TestCase):
    def test_pstr_shamstr(self):
        a = Shamsi.pstr_shamstr('2013-06-17', Shamsi.SHORT_DATE, Shamsi.LONG_DATE)
        self.assertEqual(u'27 خرداد 1392', a)

    def test_strfshamsi(self):
        d = datetime.datetime(2013, 8, 11)
        self.assertEqual(u'1392-05-20', self.get_shamsi_str(d, Shamsi.SHORT_DATE))
        d1 = datetime.datetime(2013, 8, 31)
        self.assertEqual(u'شنبه 9 شهریور 1392', self.get_shamsi_str(d1, Shamsi.FULL_DATE))
        s = Shamsi(year=1392, month=5, day=31, hour=18, minute=30, second=10).strfshamsi(Shamsi.SHORT_DATETIME)
        self.assertEqual(u'1392-05-31 18:30', s)
        d2 = datetime.datetime(2013, 9, 4, 10, 47, 50)
        self.assertEqual(u'1392/06/13 10:47:50', self.get_shamsi_str(d2, Shamsi.COMMON_DATETIME_SEC))

    def get_shamsi_str(self, d, pattern):
        shamsi = Shamsi(d)
        return shamsi.strfshamsi(pattern)

    def test_pstr_shamstr(self):
        self.assertEqual(Shamsi.pstr_shamstr('2013-06-17', Shamsi.SHORT_DATE, Shamsi.LONG_DATE), u'27 خرداد 1392')
        self.assertEqual(Shamsi.pstr_shamstr('2013-06-17 14:37', Shamsi.SHORT_DATETIME, Shamsi.SHORT_DATETIME),
                         u'1392-03-27 14:37')
        self.assertEqual(Shamsi.pstr_shamstr('2013-08-31 14:37', Shamsi.SHORT_DATETIME, Shamsi.SHORT_DATETIME),
                         u'1392-06-09 14:37')

    def test_str_to_shamsi(self):
        self.assertEqual(Shamsi.str_to_shamsi('1392-1-1 10:12', Shamsi.SHORT_DATETIME),
                         Shamsi(year=1392, month=1, day=1, hour=10, minute=12))
        self.assertEqual(Shamsi.str_to_shamsi('1392-10', '%Y-%j').pydate, datetime.datetime(2013, 3, 30))
        self.assertEqual(Shamsi.str_to_shamsi('1392-189', '%Y-%j').pydate, datetime.datetime(2013, 9, 25))
        self.assertEqual(Shamsi.str_to_shamsi('1391-366', '%Y-%j').pydate, datetime.datetime(2013, 3, 20))

    def test_get_month_name(self):
        self.assertEqual(Shamsi(year=1392, month=1, day=1, hour=10, minute=12).get_month_name(), u'فروردین')
        self.assertEqual(Shamsi(year=1391, month=12, day=30).get_month_name(), u'اسفند')
        self.assertEqual(Shamsi(year=1392, month=1, day=31).get_month_name(), u'فروردین')

    def test_get_weekday_name(self):
        self.assertEqual(Shamsi(year=1391, month=12, day=30).get_weekday_name(), u'چهارشنبه')
        self.assertEqual(Shamsi(datetime.datetime(2013, 8, 12)).get_weekday_name(), u'دوشنبه')

    def test_leap_year(self):
        self.assertEqual(Shamsi.leap_year(1387), True)
        self.assertEqual(Shamsi.leap_year(1391), True)
        self.assertEqual(Shamsi.leap_year(1392), False)

    def test_get_day_of_year(self):
        self.assertEqual(Shamsi(year=1391, month=12, day=30).get_day_of_year(), 366)
        self.assertEqual(Shamsi(year=1392, month=1, day=20).get_day_of_year(), 20)
        self.assertEqual(Shamsi(year=1392, month=2, day=3).get_day_of_year(), 34)
        self.assertEqual(Shamsi(year=1392, month=7, day=3).get_day_of_year(), 189)

    def test_get_week_number(self):
        self.assertEqual(Shamsi(year=1391, month=12, day=30).get_week_number(), 52)
        self.assertEqual(Shamsi(year=1391, month=12, day=25).get_week_number(), 51)
        self.assertEqual(Shamsi(year=1392, month=1, day=20).get_week_number(), 3)
        self.assertEqual(Shamsi(year=1392, month=1, day=30).get_week_number(), 4)
        self.assertEqual(Shamsi(year=1392, month=2, day=3).get_week_number(), 5)
        self.assertEqual(Shamsi(year=1392, month=7, day=3).get_week_number(), 27)

    def test_week_day_before(self):
        d = Shamsi(year=1392, month=5, day=21)
        self.assertEqual(d.week_day_before(0), Shamsi(year=1392, month=5, day=19))
        self.assertEqual(d.week_day_before(1), Shamsi(year=1392, month=5, day=20))
        self.assertEqual(d.week_day_before(2), Shamsi(year=1392, month=5, day=21))
        self.assertEqual(d.week_day_before(3), Shamsi(year=1392, month=5, day=15))
        self.assertEqual(d.week_day_before(4), Shamsi(year=1392, month=5, day=16))
        self.assertEqual(d.week_day_before(5), Shamsi(year=1392, month=5, day=17))
        self.assertEqual(d.week_day_before(6), Shamsi(year=1392, month=5, day=18))
        d = Shamsi(year=1392, month=5, day=25)
        self.assertEqual(d.week_day_before(0), Shamsi(year=1392, month=5, day=19))
        self.assertEqual(d.week_day_before(1), Shamsi(year=1392, month=5, day=20))
        self.assertEqual(d.week_day_before(2), Shamsi(year=1392, month=5, day=21))
        self.assertEqual(d.week_day_before(3), Shamsi(year=1392, month=5, day=22))
        self.assertEqual(d.week_day_before(4), Shamsi(year=1392, month=5, day=23))
        self.assertEqual(d.week_day_before(5), Shamsi(year=1392, month=5, day=24))
        self.assertEqual(d.week_day_before(6), Shamsi(year=1392, month=5, day=25))
        d = Shamsi(year=1392, month=5, day=1)
        self.assertEqual(d.week_day_before(0), Shamsi(year=1392, month=4, day=29))
        self.assertEqual(d.week_day_before(1), Shamsi(year=1392, month=4, day=30))
        self.assertEqual(d.week_day_before(2), Shamsi(year=1392, month=4, day=31))
        self.assertEqual(d.week_day_before(3), Shamsi(year=1392, month=5, day=1))
        self.assertEqual(d.week_day_before(4), Shamsi(year=1392, month=4, day=26))
        self.assertEqual(d.week_day_before(5), Shamsi(year=1392, month=4, day=27))
        self.assertEqual(d.week_day_before(6), Shamsi(year=1392, month=4, day=28))

    def test_get_day_of_shamsi_month(self):
        dt = datetime.datetime(2013, 9, 4)
        self.assertEqual(Shamsi(dt.date()).get_day_of_shamsi_month(1), datetime.datetime(2013, 8, 23))

        dt = datetime.datetime(2013, 9, 4)
        self.assertEqual(Shamsi(dt.date()).get_day_of_shamsi_month(2), datetime.datetime(2013, 8, 24))

        dt = datetime.datetime(2013, 9, 4)
        self.assertEqual(Shamsi(dt.date()).get_day_of_shamsi_month(10), datetime.datetime(2013, 9, 1))

    def test_get_day_of_shamsi_year(self):
        dt = datetime.datetime(2013, 9, 4)
        self.assertEqual(Shamsi(dt.date()).get_day_of_shamsi_year(), datetime.datetime(2013, 3, 21))

        dt = datetime.datetime(2013, 9, 4)
        self.assertEqual(Shamsi(dt.date()).get_day_of_shamsi_year(10), datetime.datetime(2013, 3, 30))

        dt = datetime.datetime(2013, 9, 4)
        self.assertEqual(Shamsi(dt.date()).get_day_of_shamsi_year(100), datetime.datetime(2013, 6, 28))

    def test_pdatetime(self):
        dt = datetime.datetime(2013, 9, 24)
        self.assertEqual(pdate(dt), u'2 مهر 1392')
        dt = datetime.date(2013, 9, 24)
        self.assertEqual(pdate(dt), u'2 مهر 1392')
        dt = datetime.datetime(2013, 9, 24, 17, 50)
        self.assertEqual(pdate(dt), u'2 مهر 1392 17:50')
