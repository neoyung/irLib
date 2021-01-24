from irLib.instruments.instrument import instrument
from irLib.helpers.schedule import period
from irLib.instruments.legs import fixLeg, floatLeg


class swap(instrument):
    def __init__(self, tradeDate, spotLag=period(0, 'day'), position='long', *legs):
        super().__init__(tradeDate, spotLag, position)
        self.legs = legs

    def setPricingEngine(self, discountCurve):
        self.discountCurve = discountCurve
        self.pricingEngine = self.discountCurve
        for leg in self.legs:
            leg.setPricingEngine(discountCurve)

    def calculateNPV(self, day):
        super().calculateNPV()
        NPV = 0
        for leg in self.legs:
            NPV += leg.calculateNPV(day)
        return NPV * self.longShort

    def isExpired(self, day):
        return all([leg.isExpired(day) for leg in self.legs])


class vanillaSwap(swap):
    def __init__(self, tradeDate, payer, fixSchedule, floatSchedule, floatingCurve, discountCurve=None, spotLag=period(0, 'day'), swapRate=None):
        assert payer in ('payer', 'receiver'), 'payer or receiver?'
        self.payer = payer
        self.position = 'long' if self.payer == 'payer' else 'short'

        self.floatLeg = floatLeg(
            tradeDate, floatingCurve, floatSchedule, spotLag)
        self.fixLeg = fixLeg(tradeDate, 1., fixSchedule, spotLag)
        super().__init__(tradeDate, spotLag, self.position, self.fixLeg, self.floatLeg)

        if swapRate is None:
            assert discountCurve is not None, 'need discount curve to determine swap rate'
            super().setPricingEngine(discountCurve)
            self.dayCount = self.discountCurve.dayCount
            self.tenor = self.dayCount.getYearFrac(min(self.floatLeg.schedule.startDate, self.fixLeg.schedule.startDate),
                                                   max(self.floatLeg.schedule.terminationDate, self.fixLeg.schedule.terminationDate))
            self.swapRate = self.floatLeg.calculateNPV(
                self.tradeDate) / self.fixLeg.calculateNPV(self.tradeDate)
        else:
            self.swapRate = swapRate

        self.fixLeg.rate = self.swapRate
        self.fixLeg.position = 'short'
        self.fixLeg.longShort = -1
