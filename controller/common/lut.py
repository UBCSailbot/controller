import numpy as np
from scipy import interpolate


class LUT:
    def __init__(self, lookup_table: list, interpolation_method: str = "linear"):
        self.__table = np.array(lookup_table)
        self.__interpolation = interpolation_method

        match self.__interpolation:
            case "linear":
                self.__method = self.__linearInterpolation
            case "spline":
                self.__method = self.__splineInterpolation
            case _:
                raise ValueError(self.__interpolation + " is an unknown interpolation method!")

    def __call__(self, x: float) -> float:
        return self.__method(x)

    def __linearInterpolation(self, x: float) -> float:
        return np.interp(x, self.__table[:, 0], self.__table[:, 1])

    def __splineInterpolation(self, x: float) -> float:
        cs = interpolate.CubicSpline(self.__table[:, 0], self.__table[:, 1])
        return cs(x)
