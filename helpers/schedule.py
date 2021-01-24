from dateutil.relativedelta import relativedelta
from irLib.marketConvention.roll import roll, preceding
import pandas as pd


class period:
    def __init__(self, n, timeUnit):
        assert isinstance(n, int)
        assert timeUnit in ('year', 'month', 'day')

        self.n = n
        self.timeUnit = timeUnit

        if timeUnit == 'year':
            self.relativeTimeDelta = relativedelta(years=n)
        elif timeUnit == 'month':
            self.relativeTimeDelta = relativedelta(months=n)
        else:
            self.relativeTimeDelta = relativedelta(days=n)


class schedule:
    def __init__(self, startDate, terminationDate, howOften, howToAdjust):
        assert isinstance(howOften, period)
        assert isinstance(howToAdjust, roll)

        self.startDate = startDate
        self.terminationDate = terminationDate
        self.howOften = howOften

        endDate = self.startDate + self.howOften.relativeTimeDelta
        assert endDate <= self.terminationDate, 'first payment date has to smaller than or equal to termination date'
        self.howToAdjust = howToAdjust

        self.dates = []  # theoretical payment date
        self.startDates = []  # actual start date of that period of payment as a business date
        self.startDates.append(self.howToAdjust.apply(startDate))
        self.endDates = []  # actual end date of that period of payment as a business date
        while endDate <= self.terminationDate:
            self.dates.append(endDate)
            adjustedEndDate = self.howToAdjust.apply(endDate)
            self.endDates.append(adjustedEndDate)
            self.startDates.append(adjustedEndDate)
            endDate += self.howOften.relativeTimeDelta
        self.startDates = self.startDates[:-1]

    def table(self):
        return pd.DataFrame({'dates': self.dates,
                             'start_dates': self.startDates,
                             'end_dates': self.endDates})


class floatingSchedule(schedule):
    def __init__(self, startDate, terminationDate, howOften, howToAdjust, fixedDateLag):
        super().__init__(startDate, terminationDate, howOften, howToAdjust)
        assert isinstance(fixedDateLag, period)
        
        self.fixedDateLag = fixedDateLag

        # the fixing date has to be a business date to be consistent with market
        # and before the payment date to be sensible
        p = preceding(self.howToAdjust.countryName)
        self.fixingDates = [p.apply(
            startDate - self.fixedDateLag.relativeTimeDelta) for startDate in self.startDates]

    def table(self):
        return pd.DataFrame({'dates': self.dates, 'start_dates': self.startDates,
                             'end_dates': self.endDates, 'fixing_dates': self.fixingDates})
