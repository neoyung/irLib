from abc import ABC, abstractmethod
from datetime import date, timedelta
import calendar
import datetime as dt


class dayCount(ABC):
    @abstractmethod
    def getYearFrac(self, date1, date2):
        assert isinstance(date1, date), 'wrap in date object'
        assert isinstance(date2, date), 'wrap in date object'
        assert date1 <= date2, 'date2 has to be > date1'
        pass


class _30E_360(dayCount):
    def day_count(self, start_date, end_date):
        d1 = min(30, start_date.day)
        d2 = min(30, end_date.day)

        return 360 * (end_date.year - start_date.year) \
            + 30 * (end_date.month - start_date.month) \
            + d2 - d1

    def getYearFrac(self, start_date, end_date):
        super().getYearFrac(start_date, end_date)
        return self.day_count(start_date, end_date) / 360.0


class _30_360(dayCount):
    def day_count(self, start_date, end_date):
        d1 = min(30, start_date.day)
        d2 = min(d1, end_date.day) if d1 == 30 else end_date.day
        
        return 360*(end_date.year - start_date.year)\
            + 30*(end_date.month - start_date.month)\
            + d2 - d1

    def getYearFrac(self, start_date, end_date):
        super().getYearFrac(start_date, end_date)
        return self.day_count(start_date, end_date) / 360.0



class ACT_360(dayCount):
    # standard money market day count convention
    def day_count(self, start_date, end_date):
        return (end_date - start_date).days


    def getYearFrac(self, start_date, end_date):
        super().getYearFrac(start_date, end_date)
        return self.day_count(start_date, end_date) / 360.0


class ACT_365(dayCount):
    # english money market convention
    def day_count(self,start_date, end_date):
        return (end_date - start_date).days


    def getYearFrac(self, start_date, end_date):
        super().getYearFrac(start_date, end_date)
        return self.day_count(start_date, end_date) / 365.0


class ACT_ACT(dayCount):
    def day_count(self,start_date, end_date):
        return (end_date - start_date).days


    def getYearFrac(self, start_date, end_date):
        super().getYearFrac(start_date, end_date)
        if start_date == end_date:
            return 0.0

        start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
        end_date = dt.datetime.combine(end_date, dt.datetime.min.time())
        
        start_year = start_date.year
        end_year = end_date.year
        year_1_diff = 366 if calendar.isleap(start_year) else 365
        year_2_diff = 366 if calendar.isleap(end_year) else 365

        total_sum = end_year - start_year - 1
        diff_first = dt.datetime(start_year + 1, 1, 1) - start_date
        total_sum += diff_first.days / year_1_diff
        diff_second = end_date - dt.datetime(end_year, 1, 1)
        total_sum += diff_second.days / year_2_diff

        return total_sum
