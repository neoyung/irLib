from abc import ABC, abstractmethod
from irLib.helpers.schedule import period
from datetime import date


class instrument(ABC):
    def __init__(self, tradeDate, spotLag, position):
        assert isinstance(tradeDate, date)
        assert isinstance(
            spotLag, period), 'define spot lag as a period obj from helpers'
        assert position in ('long', 'short'), 'long or short?'
        
        self.tradeDate = tradeDate
        self.spotLag = spotLag
        self.settlementDate = self.tradeDate + self.spotLag.relativeTimeDelta
        self.position = position
        self.longShort = (1 if self.position == 'long' else -1)
        self.pricingEngine = None

    @abstractmethod
    def setPricingEngine(self):
        pass

    @abstractmethod
    def calculateNPV(self):
        assert self.pricingEngine is not None, 'set pricing engine first'
        pass

    @abstractmethod
    def isExpired(self):
        pass
