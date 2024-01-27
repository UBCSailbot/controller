import numpy as np
from scipy import interpolate


class LUT:
    """
    Class for performing look-up table interpolation.

    Methods:
        __init__: Initializes the LUT object with lookup table data and interpolation method.
        __call__: Calls the interpolation method with the given input.
    """

    def __init__(self, lookup_table: list, interpolation_method: str = "linear"):
        """
        Initializes the LUT object.

        Args:
            lookup_table (list): A list of tuples or lists containing x-y data points for
            interpolation. Format is [[x-values],[y-values]]
            interpolation_method (str): Interpolation method to use. Default is "linear".

        Raises:
            ValueError: If the specified interpolation method is unknown.
        """
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
        """
        Calls the interpolation method with the given input.

        Args:
            x (float): The input value to interpolate.

        Returns:
            float: The interpolated value using the interpolation method defined when LUT instance
            creation.
        """
        return self.__method(x)

    def __linearInterpolation(self, x: float) -> float:
        return np.interp(x, self.__table[:, 0], self.__table[:, 1])

    def __splineInterpolation(self, x: float) -> float:
        cs = interpolate.CubicSpline(self.__table[:, 0], self.__table[:, 1])
        return cs(x)
