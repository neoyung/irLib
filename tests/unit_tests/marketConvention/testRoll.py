import unittest
from datetime import date
from irLib.marketConvention.roll import (
    following,
    preceding,
    modifiedFollowing,
    EOM
)

test_location = "HongKong"
holiday = date(2020, 6, 25)
sunday = date(2020, 6, 28)
saturday = date(2020, 6, 27)


class testRoll(unittest.TestCase):
    def testFollowing(self):
        r = following(test_location)
        self.assertEqual(r.apply(holiday), date(2020, 6, 26))
        self.assertEqual(r.apply(sunday), date(2020, 6, 29))
        self.assertEqual(r.apply(saturday), date(2020, 6, 29))

    def testPreceding(self):
        r = preceding(test_location)
        self.assertEqual(r.apply(holiday), date(2020, 6, 24))
        self.assertEqual(r.apply(sunday), date(2020, 6, 26))
        self.assertEqual(r.apply(saturday), date(2020, 6, 26))

    def testModifiedFollowing(self):
        r = modifiedFollowing(test_location)
        self.assertEqual(r.apply(holiday), date(2020, 6, 26))
        self.assertEqual(r.apply(sunday), date(2020, 6, 29))
        self.assertEqual(r.apply(saturday), date(2020, 6, 29))

    def testEOM(self):
        r = EOM(test_location)
        self.assertEqual(r.apply(holiday), date(2020, 6, 30))
        self.assertEqual(r.apply(sunday), date(2020, 6, 30))
        self.assertEqual(r.apply(saturday), date(2020, 6, 30))
