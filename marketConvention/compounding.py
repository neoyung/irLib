from abc import ABC, abstractmethod
import numpy as np


class compounding(ABC):
    @abstractmethod
    def getRate(self, discountFactor, yearFrac):
        pass

    @abstractmethod
    def getDF(self, rate, yearFrac):
        pass


class continuouslyCompounded(compounding):
    def getRate(self, discountFactor, yearFrac):
        return -np.log(discountFactor) / yearFrac

    def getDF(self, rate, yearFrac):
        return np.exp(-rate * yearFrac)


class simplyCompounded(compounding):
    def getRate(self, discountFactor, yearFrac):
        return (1 - discountFactor) / (yearFrac * discountFactor)

    def getDF(self, rate, yearFrac):
        return 1 / (1 + rate * yearFrac)


class annually_k_Spot(compounding):
    def __init__(self, k=1):
        self.k = k

    def getRate(self, discountFactor, yearFrac):
        return self.k / discountFactor ** (1 / (self.k * yearFrac)) - self.k

    def getDF(self, rate, yearFrac):
        return (1 + rate / self.k) ** (-self.k * yearFrac)
