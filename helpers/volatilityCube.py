from irLib.mathTools.estimationEngine import linearInterpolatorND
import numpy as np


class volatilityCube:
    def __init__(self, tenorIndex, strikeIndex, time2MaturityIndex, volatilityValues):
        self.tenorIndex = tenorIndex
        self.strikeIndex = strikeIndex
        self.time2MaturityIndex = time2MaturityIndex
        
        assert len(volatilityValues) == len(tenorIndex) * len(strikeIndex) * \
            len(time2MaturityIndex), 'no of vol. values doesnt match dimensions'
        self.values = volatilityValues
        self.linearInterpolator = None

    def getVol(self, tenor, strike, time2Maturity):
        assert tenor >= min(self.tenorIndex) and tenor <= max(self.tenorIndex)\
            and strike >= min(self.strikeIndex) and strike <= max(self.strikeIndex)\
            and time2Maturity >= min(self.time2MaturityIndex) and time2Maturity <= max(self.time2MaturityIndex), 'no extrapolation allowed'

        if self.linearInterpolator is None:
            xv, yv, zv = np.meshgrid(
                self.tenorIndex, self.strikeIndex, self.time2MaturityIndex)
            self.points = np.vstack([xv.ravel(), yv.ravel(), zv.ravel()]).T
            self.linearInterpolator = linearInterpolatorND(
                self.points, self.values)

        return self.linearInterpolator.getValues([tenor, strike, time2Maturity])
