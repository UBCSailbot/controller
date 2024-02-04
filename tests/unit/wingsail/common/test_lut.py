import math

import numpy as np
import pytest
from scipy import interpolate

from controller.common.lut import LUT


class TestLUT:
    # Intialize lookup table
    look_up_table = [[50000, 5.75], [100000, 6.75], [200000, 7], [500000, 9.75], [1000000, 10]]

    def test_LUT_constructor(self):
        # set up
        testLUT = LUT(self.look_up_table)

        # test that LUT return a known value
        assert math.isclose(testLUT(50000), 5.75)

    def test_unknown_interpolation_exception(self):
        with pytest.raises(ValueError):
            testLUT = LUT(self.look_up_table, "gabagool")

    def test_invalid_table_exception(self):
        invalid_table1 = [[10000, 10000, 10000], [1, 1, 1]]
        invalid_table2 = [10000, 10000, 10000]
        invalid_table3 = [[0, 1], 10000, 10000]

        with pytest.raises(ValueError):
            testLUT = LUT(invalid_table1)

        with pytest.raises(ValueError):
            testLUT = LUT(invalid_table2)

        with pytest.raises(ValueError):
            testLUT = LUT(invalid_table3)

    @pytest.mark.parametrize("linear_test_values", list(range(50000, 1100000, 10000)))
    def test_linear_interpolation(self, linear_test_values):
        # set up
        testLUT = LUT(self.look_up_table)
        table = np.array(self.look_up_table)

        # Test that LUT returns same values as np linear interpolate function
        assert math.isclose(
            testLUT(linear_test_values), np.interp(linear_test_values, table[:, 0], table[:, 1])
        )

    def test_linear_extrapolation(self):
        testLUT = LUT(self.look_up_table)
        # Test that linear interpolation does not extrapolate
        assert math.isclose(testLUT(10000), 5.75)
        assert math.isclose(testLUT(2000000), 10)

    @pytest.mark.parametrize("spline_test_values", list(range(10000, 2100000, 10000)))
    def test_spline_interpolation_extrapolation(self, spline_test_values):
        testLUT = LUT(self.look_up_table, "spline")
        table = np.array(self.look_up_table)
        cs = interpolate.CubicSpline(table[:, 0], table[:, 1])

        # Test that LUT returns same values as cubic interpolate function
        assert math.isclose(testLUT(spline_test_values), cs(spline_test_values))
