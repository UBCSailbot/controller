# import pytest

import numpy as np
from scipy import interpolate

from controller.common.lut import LUT


class TestLUT:
    # Intialize lookup table
    look_up_table = [[50000, 5.75], [100000, 6.75], [200000, 7], [500000, 9.75], [1000000, 10]]

    def test_LUT_constructor(self):
        # set up
        testLUT = LUT(self.look_up_table)

        # test that LUT return a known value
        assert testLUT(50000) == 5.75

    def test_unknown_interpolation_exception(self):
        try:
            testLUT = LUT(self.look_up_table, "gabagool")
            assert False  # failure: constructor accepted deli meat interpolation method

        except ValueError:
            assert True

        except:
            assert False  # failure: constructor threw wrong exception

    def test_linear_interpolation(self):
        # set up
        testLUT = LUT(self.look_up_table)
        table = np.array(self.look_up_table)
        test_values = list(range(50000, 1100000, 10000))

        # Test that linear interpolation does not extrapolate
        assert testLUT(10000) == 5.75
        assert testLUT(2000000) == 10

        # Test that LUT returns same values as np linear interpolate function
        for value in test_values:
            assert testLUT(value) == np.interp(value, table[:, 0], table[:, 1])

    def test_spline_interpolation(self):
        testLUT = LUT(self.look_up_table, "spline")
        table = np.array(self.look_up_table)
        test_values = list(range(10000, 2100000, 10000))
        cs = interpolate.CubicSpline(table[:, 0], table[:, 1])

        # Test that LUT returns same values as cubic interpolate function
        for value in test_values:
            assert testLUT(value) == cs(value)
