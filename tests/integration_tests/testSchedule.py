import unittest
from datetime import date
from irLib.helpers.schedule import period, schedule, floatingSchedule
from irLib.marketConvention.roll import following
import pandas as pd


startDate = date(2020, 6, 1)
terminationDate = date(2020, 6, 30)
howOften = period(3, 'day')
howToAdjust = following('HongKong')
fixedDateLag = period(1, 'day')
s = schedule(startDate, terminationDate, howOften, howToAdjust)
fS = floatingSchedule(startDate, terminationDate,
                      howOften, howToAdjust, fixedDateLag)

sch = pd.read_csv('irLib/tests/integration_tests/scheduleCSV/Schedule.csv')
fSch = pd.read_csv('irLib/tests/integration_tests/scheduleCSV/FSchedule.csv')


class testSchedule(unittest.TestCase):
    """ Testing the generated payment schedule to see if it got the business dates right """

    def testS(self):
        df = s.table()
        self.assertCountEqual(list(map(str, df.start_dates)), sch.start_dates)
        self.assertCountEqual(list(map(str, df.end_dates)), sch.end_dates)

    def testFS(self):
        df = fS.table()
        self.assertCountEqual(list(map(str, df.start_dates)), fSch.start_dates)
        self.assertCountEqual(list(map(str, df.end_dates)), fSch.end_dates)
        self.assertCountEqual(
            list(map(str, df.fixing_dates)), fSch.fixing_dates)
