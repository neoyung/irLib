from datetime import date
import numpy as np
from irLib.marketConvention.dayCount import (ACT_360, ACT_365,
                                             ACT_ACT, _30_360,
                                             _30E_360)
from unittest import TestCase
import datetime

""" Testing the result against result mentioned in a reference book """
date1 = date(2008, 2, 1)
date2 = date(2009, 5, 31)


class ACT_360Test(TestCase):
    
    start_date = datetime.date(2010, 1, 13)
    end_date = datetime.date(2012, 1, 3)

    def test_day_count(self):
        # Case 1: test day count for same date
        self.assertEqual(
            ACT_360().day_count(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test day count for arbitrary date difference
        self.assertEqual(
            ACT_360().day_count(self.start_date, self.end_date),
            720
        )

    def test_year_fraction(self):
        # Case 1: test year fraction for same date
        self.assertEqual(
            ACT_360().getYearFrac(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test year fraction for arbitrary date difference
        self.assertEqual(
            ACT_360().getYearFrac(self.start_date, self.end_date),
            2.0
        )

    def test_ACT_360(self):
        dC = ACT_360()
        self.assertEqual(np.round(dC.getYearFrac(date1, date2), 5), 1.34722)


class ACT_365Test(TestCase):

    start_date = datetime.date(2010, 1, 13)
    end_date = datetime.date(2012, 1, 13)

    def test_day_count(self):
        # Case 1: test day count for same date
        self.assertEqual(
            ACT_365().day_count(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test day count for arbitrary date difference
        self.assertEqual(
            ACT_365().day_count(self.start_date, self.end_date),
            730
        )

    def test_year_fraction(self):
        # Case 1: test year fraction for same date
        self.assertEqual(
            ACT_365().getYearFrac(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test year fraction for arbitrary date difference
        self.assertEqual(
            ACT_365().getYearFrac(self.start_date, self.end_date),
            2.0
        )

    def test_ACT_365(self):
        dC = ACT_365()
        self.assertEqual(np.round(dC.getYearFrac(date1, date2), 5), 1.32877)


class ACT_ACTTest(TestCase):

    start_date = datetime.date(2010, 1, 13)
    end_date = datetime.date(2014, 1, 13)

    def test_day_count(self):
        # Case 1: test day count for same date
        self.assertEqual(
            ACT_ACT().day_count(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test day count for arbitrary date difference
        self.assertEqual(
            ACT_ACT().day_count(self.start_date, self.end_date),
            1461
        )

    def test_year_fraction(self):
        # Case 1: test year fraction for same date
        self.assertEqual(
            ACT_ACT().getYearFrac(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test year fraction for arbitrary date difference
        self.assertEqual(
            ACT_ACT().getYearFrac(self.start_date, self.end_date),
            4.0
        )

    def test_ACT_ACT(self):
        dC = ACT_ACT()
        self.assertEqual(np.round(dC.getYearFrac(date1, date2), 5), 1.32626)


class _30_360Test(TestCase):

    start_date = datetime.date(2010, 1, 13)
    end_date = datetime.date(2012, 1, 13)

    def test_day_count(self):
        # Case 1: test day count for same date
        self.assertEqual(
            _30_360().day_count(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test day count for arbitrary date difference
        self.assertEqual(
            _30_360().day_count(self.start_date, self.end_date),
            720
        )

    def test_year_fraction(self):
        # Case 1: test year fraction for same date
        self.assertEqual(
            _30_360().getYearFrac(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test year fraction for arbitrary date difference
        self.assertEqual(
            _30_360().getYearFrac(self.start_date, self.end_date),
            2.0
        )

    def test_30_360US(self):
        dC = _30_360()
        self.assertEqual(np.round(dC.getYearFrac(date1, date2), 5), 1.33333)


class _30E_360Test(TestCase):

    start_date = datetime.date(2010, 8, 31)
    end_date = datetime.date(2011, 2, 28)

    def test_day_count(self):
        # Case 1: test day count for same date
        self.assertEqual(
            _30E_360().day_count(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test day count for arbitrary date difference
        self.assertEqual(
            _30E_360().day_count(self.start_date, self.end_date),
            178.0
        )

    def test_year_fraction(self):
        # Case 1: test year fraction for same date
        self.assertEqual(
            _30E_360().getYearFrac(self.start_date, self.start_date),
            0.0
        )

        # Case 2: test year fraction for arbitrary date difference
        self.assertEqual(
            _30E_360().getYearFrac(self.start_date, self.end_date),
            178/360.
        )

    def test_30E_360(self):
        dC = _30E_360()
        self.assertEqual(np.round(dC.getYearFrac(date1, date2), 5), 1.33056)
