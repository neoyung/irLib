import unittest
from datetime import date
from irLib.helpers.schedule import period, schedule, floatingSchedule
from irLib.marketConvention.roll import following
from irLib.marketConvention.dayCount import ACT_ACT
from irLib.marketConvention.compounding import annually_k_Spot
import numpy as np
from irLib.helpers.yieldCurve import discountCurve, forwardCurve
from irLib.instruments.swap import vanillaSwap


# set schedule
startDate = tradeDate = date(2020, 7, 1)
terminationDate = date(2022, 7, 1)  # a 2 year bond
howOften = period(6, 'month')  # semi-annually
howToAdjust = following('HongKong')
fixedDateLag = period(1, 'day')
s = schedule(startDate, terminationDate, howOften, howToAdjust)
fS = floatingSchedule(startDate, terminationDate, howOften, howToAdjust, fixedDateLag)

# set synthetic data
timeIndex = [1, 2, 3, 4, 5]
flatR = 0.03
dF = ((flatR + 1) ** -np.arange(1, 6)).tolist()
forwardRates = (flatR * np.ones(5)).tolist()

# set discountCurve and LiborCurve (forward rate curve)
alias_disC = 'disC'
alias_forC = 'forC'
referenceDate = date(2018, 1, 1)
dayCount = ACT_ACT()
compounding = annually_k_Spot()
allowExtrapolation = True
disC = discountCurve(alias_disC, referenceDate, dayCount, compounding, allowExtrapolation)
disC.values = dF
disC.timeIndex = timeIndex

forwardC = forwardCurve(alias_forC, referenceDate, dayCount, compounding, allowExtrapolation)
forwardC.values = forwardRates
forwardC.timeIndex = timeIndex

# fix leg rate
fixedRate = 0.03


class testVanillaSwap(unittest.TestCase):
    def testPayerSwap(self):
        """ testing the NPV of a vanilla swap should have a NPV = 0 as seen at trade date (fair value) """
        
        vanillaS = vanillaSwap(tradeDate, 'payer', s, fS, forwardC, disC)
        self.assertEqual(np.round(vanillaS.swapRate, 3), flatR)
        self.assertCountEqual(np.round([vanillaS.calculateNPV(date(2018 + d, 7, 1)) for d in range(5)], 5), np.zeros(5))

    def testReceiverSwap(self):
        """ testing the net position from a receiver and payer swap is 0 at all time """

        payer = vanillaSwap(tradeDate, 'payer', s, fS, forwardC, swapRate=0.05)
        payer.setPricingEngine(disC)

        receiver = vanillaSwap(tradeDate, 'receiver', s, fS, forwardC, swapRate=0.05)
        receiver.setPricingEngine(disC)
        
        self.assertCountEqual(np.round(np.array([payer.calculateNPV(date(2018 + d, 7, 1)) for d in range(5)]) \
            + np.array([receiver.calculateNPV(date(2018 + d, 7, 1)) for d in range(5)]), 8), np.zeros(5))
