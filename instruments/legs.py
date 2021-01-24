from irLib.instruments.instrument import instrument
from irLib.helpers.schedule import period, schedule as sch, floatingSchedule as fSch
from irLib.helpers.yieldCurve import forwardCurve as forC, discountCurve as disC
from abc import abstractmethod


class leg(instrument):
    def __init__(self, tradeDate, rate, schedule, spotLag, position):
        super().__init__(tradeDate, spotLag, position)
        assert isinstance(schedule, sch)
        self.rate = rate
        self.schedule = schedule

    def setPricingEngine(self, discountCurve):
        assert isinstance(discountCurve, disC)
        self.discountCurve = discountCurve
        self.pricingEngine = self.discountCurve
        self.dayCount = self.discountCurve.dayCount

    def isExpired(self, day):
        return day > self.schedule.endDates[-1]


class fixLeg(leg):
    def __init__(self, tradeDate, fixedRate, schedule, spotLag=period(0, 'day'), position='long'):
        assert isinstance(fixedRate, int) or isinstance(fixedRate, float)
        super().__init__(tradeDate, fixedRate, schedule, spotLag, position)

    def calculateNPV(self, day):
        super(leg, self).calculateNPV()

        NPV = 0
        futurePaymentDates = [
            paymentDate for paymentDate in self.schedule.endDates if paymentDate >= day]
        lastPaymentDate_YF = day if day >= self.schedule.startDates[
            0] else self.schedule.startDates[0]

        for paymentDate in futurePaymentDates:
            dF = self.discountCurve.getRate(day, paymentDate)
            yearFrac = self.dayCount.getYearFrac(
                lastPaymentDate_YF, paymentDate)
            NPV += dF * yearFrac
            lastPaymentDate_YF = paymentDate

        return self.rate * NPV * self.longShort


class floatLeg(leg):
    def __init__(self, tradeDate, floatingCurve, floatingSchedule, spotLag=period(0, 'day'), position='long'):
        assert isinstance(floatingCurve, forC)
        assert isinstance(
            floatingSchedule, fSch), 'define floating schedule using floating schedule obj from helpers'
        super().__init__(tradeDate, floatingCurve, floatingSchedule, spotLag, position)

    def calculateNPV(self, day):
        super(leg, self).calculateNPV()

        NPV = 0
        futureFixingAndPaymentDates = [(self.schedule.fixingDates[Id], self.schedule.startDates[Id], paymentDate)
                                       for Id, paymentDate in enumerate(self.schedule.endDates) if paymentDate >= day]
        lastPaymentDate_YF = day if day >= self.schedule.startDates[
            0] else self.schedule.startDates[0]

        for fixingDate, startDate, paymentDate in futureFixingAndPaymentDates:
            dF = self.discountCurve.getRate(day, paymentDate)
            yearFrac = self.dayCount.getYearFrac(
                lastPaymentDate_YF, paymentDate)
            floatingRate = self.rate.getRate(
                fixingDate, startDate, paymentDate)
            NPV += dF * yearFrac * floatingRate
            lastPaymentDate_YF = paymentDate

        return NPV * self.longShort
