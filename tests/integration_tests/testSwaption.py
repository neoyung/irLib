import unittest
from datetime import date
from irLib.helpers.schedule import period, schedule, floatingSchedule
from irLib.marketConvention.roll import following
from irLib.marketConvention.dayCount import _30_360
from irLib.marketConvention.compounding import annually_k_Spot
import numpy as np
from irLib.helpers.yieldCurve import discountCurve, forwardCurve
from irLib.instruments.swap import vanillaSwap
from irLib.instruments.swaption import vanillaSwaption
from irLib.helpers.volatilityCube import volatilityCube
from irLib.mathTools.pricingEngine import blackEngine


# set schedule
startDate = date(2020, 7, 1)
terminationDate = date(2022, 7, 1)  # tenor-2
howOften = period(6, 'month')  # semi-annually
howToAdjust = following('HongKong')
fixedDateLag = period(0, 'day')
s = schedule(startDate, terminationDate, howOften, howToAdjust)
fS = floatingSchedule(startDate, terminationDate,
                      howOften, howToAdjust, fixedDateLag)


# set synthetic data
timeIndex = np.arange(1, 6).tolist() # 5 year long term structure
flatR = 0.03
dF = ((flatR + 1) ** -np.arange(1, len(timeIndex) + 1)).tolist()
forwardRates = (flatR * np.ones(len(timeIndex))).tolist()

# set discountCurve 
alias_disC = 'disC'
alias_forC = 'forC'
referenceDate = date(2019, 1, 1) # t = 0 of yield curve
dayCount = _30_360()
compounding = annually_k_Spot()
allowExtrapolation = True
disC = discountCurve(alias_disC, referenceDate, dayCount, compounding, allowExtrapolation)
disC.values = dF
disC.timeIndex = timeIndex

# set LiborCurve (an instance of forward rate curve)
forwardC = forwardCurve(alias_forC, referenceDate, dayCount, compounding, allowExtrapolation)
forwardC.values = forwardRates
forwardC.timeIndex = timeIndex

# set vol. cube
expiryDate = startDate
volCube = volatilityCube([1, 2, 3], [0.02, 0.03, 0.04], [1, 2], np.arange(10, 28) * 0.01)

# set swap
strike = 0.03  # near money option due to interpolation methodolgy, swap rate is 0.029781
vanillaS = vanillaSwap(startDate, 'payer', s, fS, forwardC, disC)

# set swaptions
swaptionStartDate = date(2019, 1, 1) # 1.5 year swaption on a tenor-2 swap
payerSwaption = vanillaSwaption(
    swaptionStartDate, expiryDate, 'payer', strike, volCube)
payerSwaption.setUnderlying(vanillaS)
payerSwaption.setPricingEngine(blackEngine())

receiverSwaption = vanillaSwaption(
    swaptionStartDate, expiryDate, 'receiver', strike, volCube)
receiverSwaption.setUnderlying(vanillaS)
receiverSwaption.setPricingEngine(blackEngine())


class testSwaption(unittest.TestCase):
    """ Compare the payer and receiver swaption prices with online and replicatingExcel,
     difference is due to discount factor caused by dayCount, around 0.5% difference """

    def testPayerNPV(self):
        self.assertEqual(np.round(payerSwaption.calculateNPV(
            swaptionStartDate), 8), 0.00478878)

    def testReceiverNPV(self):
        self.assertEqual(np.round(receiverSwaption.calculateNPV(
            swaptionStartDate), 8), 0.00519489)

    def testBackSolverPayerVol(self):
        self.assertEqual(np.round(payerSwaption.backSolveImpliedVolatility(
            swaptionStartDate, 0.00478878), 6), 0.185)

    def testBackSolverReceiverVol(self):
        self.assertEqual(np.round(receiverSwaption.backSolveImpliedVolatility(
            swaptionStartDate, 0.00519489), 6), 0.185)
