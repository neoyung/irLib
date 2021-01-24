import unittest
from datetime import date
from irLib.helpers.schedule import period, schedule, floatingSchedule
from irLib.marketConvention.roll import following
from irLib.marketConvention.dayCount import ACT_ACT
from irLib.marketConvention.compounding import annually_k_Spot
import numpy as np
from irLib.helpers.yieldCurve import discountCurve, forwardCurve
from irLib.instruments.legs import fixLeg, floatLeg


# set schedule
startDate = tradeDate = date(2020, 7, 1)
terminationDate = date(2022, 7, 1)  # a 2 year bond
howOften = period(6, 'month')  # semi-annually
howToAdjust = following('HongKong')
fixedDateLag = period(1, 'day')
s = schedule(startDate, terminationDate, howOften, howToAdjust)
fS = floatingSchedule(startDate, terminationDate,
                      howOften, howToAdjust, fixedDateLag)

# set synthetic data
timeIndex = [1, 2, 3, 4, 5]
flatR = 0.03
dF = ((flatR + 1) ** -np.arange(1, 6)).tolist()
forwardRates = (flatR * np.ones(5)).tolist()

# set discountCurve and LiborCurve (instance of forwad rate curve)
alias_disC = 'disC'
alias_forC = 'forC'
referenceDate = date(2018, 1, 1)
dayCount = ACT_ACT()
compounding = annually_k_Spot()
allowExtrapolation = True # trigger warning if false and extrapolation is needed
disC = discountCurve(alias_disC, referenceDate, dayCount, compounding, allowExtrapolation)
disC.values = dF
disC.timeIndex = timeIndex

forwardC = forwardCurve(alias_forC, referenceDate, dayCount, compounding, allowExtrapolation)
forwardC.values = forwardRates
forwardC.timeIndex = timeIndex

# fix leg parameter
fixedRate = 0.03
fixL = fixLeg(tradeDate, fixedRate, s)
floatL = floatLeg(tradeDate, forwardC, fS)


class testLegs(unittest.TestCase):
    """ Testing its NPV in the first 3 years """
    def testFixLeg(self):
        fixL.setPricingEngine(disC)
        
        self.assertCountEqual(np.round([fixL.calculateNPV(date(2020 + d, 7, 1)) for d in range(3)], 8),
                              [0.05793798, 0.02957842, 0.00024652])

    def testFloatLeg(self):
        floatL.setPricingEngine(disC)
        # the difference from cash flow of fix leg is due to interpolation methodolgy of forward rates, 
        # as forward rate is defined by (fixDate, paymentPeriodStartDate, paymentPeriodEndDate)
        self.assertCountEqual(np.round([floatL.calculateNPV(date(2020 + d, 7, 1)) for d in range(3)], 8),
                              [0.05751394, 0.02936204, 0.00024290])
