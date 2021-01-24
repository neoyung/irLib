from irLib.instruments.instrument import instrument
from abc import abstractmethod


class option(instrument):
    def __init__(self, tradeDate, spotLag, expiryDate, position):
        self.expiryDate = expiryDate
        self.underlying = None
        super().__init__(tradeDate, spotLag, position)

    def isExpired(self, day):
        return day > self.expiryDate

    @abstractmethod
    def setUnderlying(self):
        pass
