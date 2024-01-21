class LUT:
    def __init__(self, lookup_table, interpolation_method="linear"):
        self.table = lookup_table
        self.interpolation = interpolation_method

    def __call__(self, x):
        if self.interpolation == "linear":
            return self.linearInterpolation(x)
        elif self.interpolation == "spline":
            return self.splineInterpolation(x)
        else:
            raise ValueError(self.interpolation + " is an unknown interpolation method!")

    def linearInterpolation(self, x):
        return 0

    def splineInterpolation(self, x):
        return 0
