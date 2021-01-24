from abc import abstractmethod

from irLib.instruments.option import option
from irLib.helpers.schedule import period
from irLib.instruments.swap import vanillaSwap as vanillaS
from irLib.mathTools.pricingEngine import blackStyleEngine
from irLib.helpers.volatilityCube import volatilityCube as volC
from irLib.mathTools.nonLinearSolver import nonLinearSolver1D


class swaption(option):
    def __init__(self, tradeDate, expiryDate, payer, spotLag, position):
        assert payer in ('payer', 'receiver'), 'payer or receiver?'
        self.payer = payer
        self.callOrPut = 'call' if self.payer == 'payer' else 'put'
        super().__init__(tradeDate, spotLag, expiryDate, position)

    @abstractmethod
    def calculateNPV(self, day):
        if super().isExpired(day):
            return 0.

        super(option, self).calculateNPV()
        assert self.underlying is not None, 'set underlying swap with setUnderlying method'
        pass

    @abstractmethod
    def backSolveImpliedVolatility(self):
        super(option, self).calculateNPV()
        assert self.underlying is not None, 'set underlying swap with setUnderlying method'
        pass


class vanillaSwaption(swaption):
    def __init__(self, tradeDate, expiryDate, payer, strike, volatilityCube, spotLag=period(0, 'day'), position='long'):
        super().__init__(tradeDate, expiryDate, payer, spotLag, position)
        assert isinstance(volatilityCube, volC)
        self.volatilityCube = volatilityCube
        self.strike = strike

    def setUnderlying(self, vanillaSwap):
        assert isinstance(vanillaSwap, vanillaS), 'not a vanilla swap'
        self.underlying = vanillaSwap
        assert self.underlying.discountCurve is not None, 'set a vanilla swap with discount curve'
        self.discountCurve = self.underlying.discountCurve
        self.dayCount = self.discountCurve.dayCount

    def setPricingEngine(self, pricingEngine):
        assert isinstance(
            pricingEngine, blackStyleEngine), 'Use Black or Bachelier pricing engine'
        self.pricingEngine = pricingEngine

    def calculateNPV(self, day, impliedVol=None):
        super().calculateNPV(day)

        forwardSwapRate = self.underlying.swapRate
        time2Maturity = self.dayCount.getYearFrac(day, self.expiryDate)
        if impliedVol is None:
            impliedVol = self.volatilityCube.getVol(
                self.underlying.tenor, self.strike, time2Maturity)
        self.pricingEngine.setArgument(
            forwardSwapRate, self.strike, impliedVol, time2Maturity, self.callOrPut)

        discountFactor = 0
        for startDate, endDate in zip(self.underlying.fixLeg.schedule.startDates, self.underlying.fixLeg.schedule.endDates):
            discountFactor += self.dayCount.getYearFrac(
                startDate, endDate) * self.discountCurve.getRate(day, endDate)

        return self.pricingEngine.calculate() * discountFactor * self.longShort

    def backSolveImpliedVolatility(self, day, NPV):
        super().backSolveImpliedVolatility()

        def F(impliedVol):
            return self.calculateNPV(day, impliedVol) - NPV
        return nonLinearSolver1D(F, xin=0.2, f_tol=1e-14)
