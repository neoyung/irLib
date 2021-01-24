import unittest
from datetime import date
from irLib.marketConvention.dayCount import ACT_ACT
from irLib.marketConvention.compounding import annually_k_Spot
from irLib.helpers.yieldCurve import yieldCurve, discountCurve, forwardCurve
import numpy as np


alias_disC = 'disC'
alias_forC = 'forC'
referenceDate = date(2020, 6, 26)
dayCount = ACT_ACT()
compounding = annually_k_Spot()
allowExtrapolation = False

# set synthetic data
timeIndex = [1, 2, 3, 4, 5]
flatR = 0.03
dF = ((flatR + 1) ** -np.arange(1, 6)).tolist()
forwardRates = (flatR * np.ones(5)).tolist()
spots = (flatR * np.ones(5)).tolist()
yearFrac = np.arange(1, 6).tolist()
par = (flatR * np.ones(5)).tolist()

t = date(2021, 6, 30) # try date(2021, 6, 26) will trigger extrapolation warning msg
t1 = date(2022, 6, 26)
t2 = date(2023, 6, 26)

class testYieldCurveGetRate(unittest.TestCase):
    def testDiscountCurve(self):
        disC = discountCurve(alias_disC, referenceDate,
                             dayCount, compounding, allowExtrapolation)
        disC.values = dF
        disC.timeIndex = timeIndex
        self.assertAlmostEqual(disC.getRate(t1, t2), (1 + flatR) ** -1) # almostEqual auto rounds to 7 decimals

    def testForwardCurve(self):
        forwardC = forwardCurve(alias_forC, referenceDate,
                                dayCount, compounding, allowExtrapolation)
        forwardC.values = forwardRates
        forwardC.timeIndex = timeIndex
        self.assertAlmostEqual(forwardC.getRate(t, t1, t2), flatR)

    def testSpot2Df(self):
        self.assertCountEqual(np.round(yieldCurve.spot2Df(
            spots, yearFrac, compounding), 8), np.round(dF, 8))
        self.assertCountEqual(np.round(yieldCurve.spot2Df(
            dF, yearFrac, compounding, reverse=True), 8), np.round(spots, 8))

    def testDf2Forward(self):
        self.assertCountEqual(np.round(yieldCurve.dF2Forward(
            dF, yearFrac), 8), np.round(forwardRates, 8))

    def testForward2Spot(self):
        self.assertCountEqual(np.round(yieldCurve.forward2Spot(
            forwardRates, yearFrac, compounding), 8), np.round(spots, 8))

    def testPar2Df(self):
        self.assertCountEqual(
            np.round(yieldCurve.par2Df(par, yearFrac), 8), np.round(dF, 8))
        self.assertCountEqual(np.round(yieldCurve.par2Df(
            dF, yearFrac, reverse=True), 8), np.round(par, 8))
