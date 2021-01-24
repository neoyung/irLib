from abc import ABC, abstractmethod

from irLib.mathTools.estimationEngine import linearInterpolator1D, linearExtrapolator1D
from irLib.marketConvention.dayCount import dayCount as dayC
from irLib.marketConvention.compounding import compounding as comp

from datetime import date
import numpy as np
import warnings


class yieldCurve(ABC):
    @abstractmethod
    def __init__(self, alias, referenceDate, dayCount, compounding, allowExtrapolation):
        assert isinstance(referenceDate, date)
        assert isinstance(dayCount, dayC)
        assert isinstance(compounding, comp)

        self.alias = alias
        self.referenceDate = referenceDate
        self.dayCount = dayCount
        self.compounding = compounding
        self.allowExtrapolation = allowExtrapolation

        self.dataSource = None
        self.timeIndex = None
        self.values = None
        self.interpolationEngine = None
        self.extrapolationEngine = None
        self.checkThenConvert = lambda t: t if isinstance(t, int) or isinstance(
            t, float) else self.dayCount.getYearFrac(self.referenceDate, t)
        self.yearFrac = None

    def getYearFrac(self, timeIndex):
        self.yearFrac = [self.checkThenConvert(
            timeIndex[i]) for i in range(len(timeIndex))]

    @staticmethod
    def spot2Df(values, yearFrac, compounding, reverse=False):
        if reverse:
            return [compounding.getRate(values[i], yearFrac[i]) for i in range(len(values))]

        return [compounding.getDF(values[i], yearFrac[i]) for i in range(len(values))]

    @staticmethod
    def dF2Forward(dF, yearFrac):
        dF = [1] + dF
        _yearFrac = [0] + yearFrac

        return [(dF[i] / dF[i + 1] - 1) / (_yearFrac[i + 1] - _yearFrac[i]) for i in range(len(_yearFrac) - 1)]

    @staticmethod
    def forward2Spot(forwardRates, yearFrac, compounding):
        _yearFrac = [0] + yearFrac
        dF = []
        lastDf = 1

        for i in range(len(_yearFrac) - 1):
            dF.append(
                lastDf / ((_yearFrac[i + 1] - _yearFrac[i]) * forwardRates[i] + 1))
            lastDf = dF[-1]

        return yieldCurve.spot2Df(dF, yearFrac, compounding, reverse=True)

    @staticmethod
    def par2Df(values, yearFrac, reverse=False):
        _yearFrac = [0] + yearFrac
        yearFracDiff = [_yearFrac[i + 1] - _yearFrac[i]
                        for i in range(len(_yearFrac) - 1)]
        if reverse:
            return [(1 - values[i]) / np.dot(yearFracDiff[:i+1], values[:i+1]) for i in range(len(yearFracDiff))]

        parTauMatrix = np.zeros((len(yearFracDiff), len(yearFracDiff)))
        for i in range(len(yearFracDiff)):
            parTauMatrix[i, :i + 1] = values[i] * \
                np.array(yearFracDiff[:i + 1])

        return np.linalg.solve(parTauMatrix + np.identity(len(yearFracDiff)), np.ones(len(yearFracDiff))).tolist()

    def _getRate(self, t):
        t = self.checkThenConvert(t)
        if self.yearFrac is None:
            self.getYearFrac(self.timeIndex)

        if t < min(self.yearFrac) or t > max(self.yearFrac):
            if not self.allowExtrapolation:
                warnings.warn(
                    'YieldCurve setting upon initialization does not allow extrapolation but user requesting it ...')
            if self.extrapolationEngine is None:
                self.extrapolationEngine = linearExtrapolator1D(
                    self.yearFrac, self.values)
            return self.extrapolationEngine.getValues(t)

        if self.interpolationEngine is None:
            self.interpolationEngine = linearInterpolator1D(
                self.yearFrac, self.values)
        return self.interpolationEngine.getValues(t)


class discountCurve(yieldCurve):
    def __init__(self, alias, referenceDate, dayCount, compounding, allowExtrapolation):
        super().__init__(alias, referenceDate, dayCount, compounding, allowExtrapolation)
        self.type = 'discount'

    def getRate(self, t1, t2):
        assert t1 <= t2, 'discount factor not defined'

        return super()._getRate(t2) / super()._getRate(t1)


class forwardCurve(yieldCurve):
    def __init__(self, alias, referenceDate, dayCount, compounding, allowExtrapolation):
        super().__init__(alias, referenceDate, dayCount, compounding, allowExtrapolation)
        self.discountCurve = discountCurve(
            alias, referenceDate, dayCount, compounding, allowExtrapolation)
        self.type = 'forward'

    def getRate(self, t, t1, t2):
        # t: time pt where one stands, t1 ~ t2: period of interest
        if self.yearFrac is None:
            self.getYearFrac(self.timeIndex)

        if self.discountCurve.timeIndex is None:
            self.discountCurve.timeIndex = self.timeIndex
        if self.discountCurve.values is None:
            spots = yieldCurve.forward2Spot(
                self.values, self.yearFrac, self.compounding)
            self.discountCurve.values = yieldCurve.spot2Df(
                spots, self.yearFrac, self.compounding)

        t = self.checkThenConvert(t)
        t1 = self.checkThenConvert(t1)
        t2 = self.checkThenConvert(t2)
        return (self.discountCurve.getRate(t, t1) / self.discountCurve.getRate(t, t2) - 1) / (t2 - t1)
