"""Tests classes and functions in controller/wingsail/controllers.py"""

import numpy as np
import pytest

from controller.wingsail.controllers import WingsailController


class TestWingsailController:
    @pytest.fixture
    def wingsail_controller(self):
        return WingsailController()

    @pytest.mark.parametrize(
        "apparent_wind_speed, expected_reynolds_number",
        [(10.0, 985171.4622911938), (20.0, 1970342.9245823876), (5.0, 492585.7311458489)],
    )
    def test_compute_reynolds_number(
        self, wingsail_controller, apparent_wind_speed, expected_reynolds_number
    ):
        assert np.isclose(
            wingsail_controller._compute_reynolds_number(apparent_wind_speed),
            expected_reynolds_number,
        )

    @pytest.mark.parametrize(
        "reynolds_number, look_up_table, expected_desired_alpha",
        [
            (1000000, np.array([[500000, 3], [1500000, 5]]), 4),  # Test case 1
            (2000000, np.array([[1500000, 5], [2500000, 7]]), 6),  # Test case 2
            (3000000, np.array([[2500000, 7], [3500000, 9]]), 8),  # Test case 3
        ],
    )
    def test_compute_angle_of_attack(
        self, wingsail_controller, reynolds_number, look_up_table, expected_desired_alpha
    ):
        assert np.isclose(
            wingsail_controller._compute_angle_of_attack(reynolds_number, look_up_table),
            expected_desired_alpha,
        )

    @pytest.mark.parametrize(
        "desired_alpha, apparent_wind_direction, expected_trim_tab_angle",
        [
            (5, 45, 5),  # Test case 1
            (10, -30, -10),  # Test case 2
            (15, 0, 15),  # Test case 3
        ],
    )
    def test_compute_trim_tab_angle(
        self, wingsail_controller, desired_alpha, apparent_wind_direction, expected_trim_tab_angle
    ):
        assert (
            wingsail_controller._compute_trim_tab_angle(desired_alpha, apparent_wind_direction)
            == expected_trim_tab_angle
        )

    @pytest.mark.parametrize(
        "apparent_wind_speed, apparent_wind_direction, expected_trim_tab_angle",
        [
            (10, 45, 5),  # Test case 1
            (20, -30, -10),  # Test case 2
            (5, 0, 15),  # Test case 3
        ],
    )
    def test_get_trim_tab_angle(
        self,
        wingsail_controller,
        apparent_wind_speed,
        apparent_wind_direction,
        expected_trim_tab_angle,
    ):
        assert (
            wingsail_controller.get_trim_tab_angle(apparent_wind_speed, apparent_wind_direction)
            == expected_trim_tab_angle
        )
