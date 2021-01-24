from abc import ABC, abstractmethod
from scipy import interpolate
import numpy as np


class estimationEngine(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def getValues(self):
        pass


class linearInterpolator1D(estimationEngine):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.linearFunction = interpolate.interp1d(x, y)

    def getValues(self, x_prime):
        return self.linearFunction(x_prime)


class linearExtrapolator1D(estimationEngine):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.linearFunction = interpolate.interp1d(
            x, y, fill_value='extrapolate')

    def getValues(self, x_prime):
        return self.linearFunction(x_prime)


class cubicSpline1D(estimationEngine):
    def __init__(self, x, y):
        super().__init__(x, y)
        # by default, it does both of the interpolation or extrapolation
        self.polynomialFunction = interpolate.cubicSpline(x, y)

    def getValues(self, x_prime):
        return self.polynomialFunction(x_prime)


class linearInterpolator2D(estimationEngine):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z
        self.linearFunction = interpolate.interp2d(x, y, z)

    def getValues(self, x_prime, y_prime):
        return self.linearFunction(x_prime, y_prime)


class linearExtrapolator2D(estimationEngine):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z
        self.linearFunction = interpolate.interp2d(x, y, z, bounds_error=False)

    def getValues(self, x_prime, y_prime):
        return self.linearFunction(x_prime, y_prime)


class CloughTocher2DInterpolator(estimationEngine):
    # no extrapolation version of CT
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z
        points = np.concatenate(
            (np.expand_dims(x, axis=1), np.expand_dims(y, axis=1)), axis=1)
        self.CTFunction = interpolate.CloughTocher2DInterpolator(
            points, z)

    def getValues(self, x_prime, y_prime):
        points_prime = np.concatenate(
            (np.expand_dims(x_prime, axis=1), np.expand_dims(y_prime, axis=1)), axis=1)
        return self.CTFunction(points_prime)


class linearInterpolatorND(estimationEngine):
    def __init__(self, x_vector, y):
        # x_vector is of dimension (n_points, n_dims)
        super().__init__(x_vector, y)
        self.NDfunction = interpolate.LinearNDInterpolator(x_vector, y)

    def getValues(self, x_vector_prime):
        return self.NDfunction(x_vector_prime)
