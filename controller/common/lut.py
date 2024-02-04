from typing import List, Union

import numpy as np
from scipy import interpolate


class LUT:
    """
    Class for performing look-up table interpolation.

    Methods:
        __init__: Initializes the LUT object with lookup table data and interpolation method.
        __call__: Calls the interpolation method with the given input.
    """

    def __init__(
        self,
        lookup_table: Union[List[List[int | float]], np.ndarray],
        interpolation_method: str = "linear",
    ):
        """
        Initializes the LUT object.

        Args:
            lookup_table (list): A list of tuples or lists containing x-y data points for
            interpolation. Format is [[x1,y1], [x2,y2], ..., [xn,yn]]
            interpolation_method (str): Interpolation method to use. Default is "linear".

        Raises:
            ValueError: If the specified interpolation method is unknown.
        """
        if type(lookup_table) is np.ndarray:
            self.__table = lookup_table
        else:
            self.__table = np.array(lookup_table)

        self.__verifyTable(self.__table)
        self.x = self.__table[:, 0]
        self.y = self.__table[:, 1]

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
        return np.interp(x, self.x, self.y)

    def __splineInterpolation(self, x: float) -> float:
        cs = interpolate.CubicSpline(self.x, self.y)
        return cs(x)

    def __verifyTable(self, table: np.ndarray) -> None:
        if len(table.shape) == 2:
            if table.shape[1] == 2:
                return
            else:
                raise ValueError("Input table is invalid shape.")
        else:
            raise ValueError("Input table is invalid shape.")
