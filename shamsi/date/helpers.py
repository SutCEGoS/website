# -*- coding: utf-8 -*-
import datetime
from .shamsi_date import Shamsi


class Interval():
    def __init__(self, dt=None):
        self.dt = dt
        if dt is None:
            self.dt = datetime.datetime.now()

    def get_week_number(self):
        u""" شماره هفته میلادی این تاریخ را برمی گرداند.
            این تابع یکشنبه را روز اول هفته در نظر می گیرد و خروجی آن در
            سایر تابع های خود پایتون قابلیت استفاده دارد.
            شماره هفته خروجی از صفر شروع می‌شود.

            :rtype: int
        """
        return int(self.dt.strftime('%U'))

    def get_week_interval(self):
        u""" بازه‌ی شنبه‌ی زمان داده شده  تا زمان داده شده را میدهد
            :rtype:datetime.datetime
        """
        return Shamsi(self.dt).get_python_week_day_before(6), self.dt

    def month_interval(self):
        u"""بازه‌ی اول ماه شمسی تا اکنون را می‌دهد
        rtype:tuple
        :rtype:(datetime.datetime,datetime.datetime)
        """
        return Shamsi(self.dt.date()).get_day_of_shamsi_month(1), self.dt

    def year_interval(self):
        u"""
        اول سال شمسی تا اکنون را میدهد
        :rtype:(datetime.datetime,datetime.datetime)
        """
        now = datetime.datetime.now()
        # noinspection PyTypeChecker
        return Shamsi(self.dt.date()).get_day_of_shamsi_year(1), now

    def day_interval(self):
        u"""
        اول روز تا آخر روز را میدهد
        :rtype:(datetime.datetime,datetime.datetime)
        """
        # noinspection PyTypeChecker
        return datetime.datetime.combine(self.dt.date(), datetime.time.min), datetime.datetime.combine(self.dt.date(),
                                                                                                    datetime.time.max)

    def now_interval(self):
        u"""
        اول روز تا اکنون را میدهد
        :rtype:(datetime.datetime,datetime.datetime)
        """
        dt = self.dt
        return datetime.datetime(dt.year, dt.month, dt.day), dt