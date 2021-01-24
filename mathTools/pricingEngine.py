from abc import ABC, abstractmethod
from scipy.stats import norm
import numpy as np


class pricingEngine(ABC):
    @abstractmethod
    def setArgument(self):
        pass

    @abstractmethod
    def getArgument(self):
        pass

    @abstractmethod
    def calculate(self):
        pass


class blackStyleEngine(pricingEngine):
    def setArgument(self, F, K, sigma, T, callOrPut):
        assert callOrPut in ('call, put'), 'call or put?'
        self.F = F
        self.K = K
        self.sigma = sigma
        self.T = T
        self.callOrPut = callOrPut

    def getArgument(self):
        return {'F': self.F, 'K': self.K, 'sigma': self.sigma,
                'T': self.T, 'callOrPut': self.callOrPut}

    @abstractmethod
    def calculate(self):
        pass


class blackEngine(blackStyleEngine):
    def calculate(self):
        E = self.sigma * self.T ** 0.5
        d1 = (np.log(self.F / self.K) + E ** 2 / 2) / E
        d2 = d1 - E
        if self.callOrPut == 'call':
            return self.F * norm.cdf(d1) - self.K * norm.cdf(d2)
        else:
            return self.K * norm.cdf(-d2) - self.F * norm.cdf(-d1)


class bachelierEngine(blackStyleEngine):
    def calculate(self):
        d_sigma = (self.F - self.K) / (self.sigma * self.T ** 0.5)
        if self.callOrPut == 'call':
            return (norm.pdf(d_sigma) + d_sigma * norm.cdf(d_sigma)) * \
                self.sigma * self.T ** 0.5
        else:
            return (norm.pdf(d_sigma) - d_sigma * norm.cdf(-d_sigma)) * \
                self.sigma * self.T ** 0.5
