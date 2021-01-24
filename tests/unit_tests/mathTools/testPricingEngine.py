import unittest
import numpy as np
from irLib.mathTools.pricingEngine import blackEngine, bachelierEngine

F = 0.03
K = 0.032
sigma = 0.2
time2Maturity = 2
# r = 0 for easy intergration swaption pricing which just need the future
# expected value of forward swap rate over strike


class testPricingEngine(unittest.TestCase):
    def testBlack(self):
        b = blackEngine()
        b.setArgument(F, K, sigma, time2Maturity, 'call')
        self.assertEqual(np.round(b.calculate(), 9), 0.002576078)
        b.setArgument(F, K, sigma, time2Maturity, 'put')
        self.assertEqual(np.round(b.calculate(), 9), 0.004576078)

    def testBachelier(self):
        b = bachelierEngine()
        b.setArgument(F, K, sigma, time2Maturity, 'call')
        self.assertEqual(np.round(b.calculate(), 9), 0.111840738)
        b.setArgument(F, K, sigma, time2Maturity, 'put')
        self.assertEqual(np.round(b.calculate(), 9), 0.113840738)
