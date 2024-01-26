import numpy as np


class LUT:
    def __init__(self, lookup_table, interpolation_method="linear"):
        self.table = np.array(lookup_table)
        self.interpolation = interpolation_method
        # look at python "match" statement to replace below
        if self.interpolation != "linear" and self.interpolation != "spline":
            raise ValueError(self.interpolation + " is an unknown interpolation method!")

    # Devon suggestions
    # rather then if else, store a reference to the function of the interpolation you want and call
    # it here. You can define the reference in the constructor

    # make self.interpolation field private
    # also make the interpolation methods private

    # add variable and return typing
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
