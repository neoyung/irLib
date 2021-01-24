from irLib.marketConvention.compounding import (
    continuouslyCompounded, simplyCompounded, annually_k_Spot
)
import numpy as np
import unittest

yearFrac = 2.
rate = 0.03
k = 4


class testCompounding(unittest.TestCase):
    """ Testing the result against result mentioned in a reference book """

    def testContinuouslyCompounded(self):
        c = continuouslyCompounded()
        self.assertEqual(np.round(c.getDF(rate, yearFrac), 8), 0.94176453)
        self.assertEqual(np.round(c.getRate(0.94176453, yearFrac), 8), rate)

    def testSimplyCompounded(self):
        c = simplyCompounded()
        self.assertEqual(np.round(c.getDF(rate, yearFrac), 8), 0.94339623)
        self.assertEqual(np.round(c.getRate(0.94339623, yearFrac), 8), rate)

    def testAnnually_1_Spot(self):
        c = annually_k_Spot()
        self.assertEqual(np.round(c.getDF(rate, yearFrac), 8), 0.94259591)
        self.assertEqual(np.round(c.getRate(0.94259591, yearFrac), 8), rate)

    def testAnnually_k_Spot(self):
        c = annually_k_Spot(k)
        self.assertEqual(np.round(c.getDF(rate, yearFrac), 8), 0.9419754)
        self.assertEqual(np.round(c.getRate(0.9419754, yearFrac), 8), rate)
