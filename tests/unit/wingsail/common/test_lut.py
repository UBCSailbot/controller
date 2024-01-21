# import pytest

from controller.common.lut import LUT


class TestLUT:
    def test_LUT_constructor(self):
        look_up_table = [[50000, 5.75], [100000, 6.75], [200000, 7], [500000, 9.75], [1000000, 10]]
        testLUT = LUT(look_up_table)
        assert testLUT(40000) == 5.75

    # def test_linear_interpolation

    # def test_spline_interpolation

    # test_LUT_constructor
