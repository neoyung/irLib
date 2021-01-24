from abc import ABC, abstractmethod
from datetime import date, timedelta
import calendar
import holidays


class roll(ABC):
    def __init__(self, countryName):
        self.countryName = countryName
        self.countryHoliday = holidays.CountryHoliday(self.countryName)

    @staticmethod
    def isBusinessDay(day, countryHoliday):
        return (not day in countryHoliday) and day.weekday() < 5

    @abstractmethod
    def apply(self, day):
        assert isinstance(day, date)
        pass

class noRoll(roll):
    def __init__(self, countryName):
        super().__init__(countryName)

    def apply(self, day):
        super().apply(day)
        return day


class following(roll):
    def __init__(self, countryName):
        super().__init__(countryName)

    @staticmethod
    def _apply(day, countryHoliday):
        while not roll.isBusinessDay(day, countryHoliday):
            day += timedelta(days=1)
        return day

    def apply(self, day):
        super().apply(day)
        return self._apply(day, self.countryHoliday)


class preceding(roll):
    def __init__(self, countryName):
        super().__init__(countryName)

    @staticmethod
    def _apply(day, countryHoliday):
        while not roll.isBusinessDay(day, countryHoliday):
            day -= timedelta(days=1)
        return day

    def apply(self, day):
        super().apply(day)
        return self._apply(day, self.countryHoliday)


class modifiedFollowing(roll):
    def __init__(self, countryName):
        super().__init__(countryName)

    def apply(self, day):
        super().apply(day)
        if roll.isBusinessDay(day, self.countryHoliday):
            return day

        dayFollowing = following._apply(day, self.countryHoliday)
        if dayFollowing.month == day.month:
            return dayFollowing

        return preceding._apply(day, self.countryHoliday)


class EOM(roll):
    def __init__(self, countryName):
        super().__init__(countryName)

    def apply(self, day):
        super().apply(day)
        if roll.isBusinessDay(day, self.countryHoliday):
            return day

        EOMdate = calendar.monthrange(day.year, day.month)[1]
        return preceding._apply(date(day.year, day.month, EOMdate), self.countryHoliday)
