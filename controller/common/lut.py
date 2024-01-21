import numpy as np


class LUT:
    def __init__(self, lookup_table, interpolation_method="linear"):
        self.table = np.array(lookup_table)
        self.interpolation = interpolation_method
        if self.interpolation != "linear" and self.interpolation != "spline":
            raise ValueError(self.interpolation + " is an unknown interpolation method!")

    def __call__(self, x):
        if self.interpolation == "linear":
            return self.linearInterpolation(x)
        elif self.interpolation == "spline":
            return self.splineInterpolation(x)
        else:
            return 0

    def linearInterpolation(self, x):
        return np.interp(x, self.table[:, 0], self.table[:, 1])

    def splineInterpolation(self, x):
        cs = np.interpolate.CubicSpline(self.table[:, 0], self.table[:, 1])
        return cs(x)
