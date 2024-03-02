import pytest
import math
import numpy as np
from controller.common.lut import LUT
from controller.wingsail.controllers import WingsailController

# Define test data
test_lut_data = np.array([[50000, 5.75], [100000, 6.75], [200000, 7], [500000, 9.25], [1000000, 10]])
test_lut = LUT(test_lut_data)
test_chord_width = 0.14
test_kinematic_viscosity = 0.000014207


class TestWingsailController:
    """
    Tests the functionality of the WingsailController class.
    """

    @pytest.fixture
    def wingsail_controller(self):
        """
        Fixture to create an instance of WingsailController for testing.
        """
        return WingsailController(test_chord_width, test_kinematic_viscosity, test_lut)

    def test_compute_reynolds_number(self, wingsail_controller):
        """
        Tests the computation of Reynolds number.

        Args:
            wingsail_controller: Instance of WingsailController.
        """
        apparent_wind_speed = 1.0
        expected_reynolds_number = 9854.297177
        computed_reynolds_number = wingsail_controller._compute_reynolds_number(apparent_wind_speed
                                                                                )
        assert math.isclose(computed_reynolds_number, expected_reynolds_number)

    def test_compute_angle_of_attack(self, wingsail_controller):
        """
        Tests the computation of angle of attack.

        Args:
            wingsail_controller: Instance of WingsailController.
        """
        reynolds_number = 75000
        expected_desired_alpha = 6.25
        computed_desired_alpha = wingsail_controller._compute_angle_of_attack(reynolds_number
                                                                              , test_lut)
        assert math.isclose(computed_desired_alpha, expected_desired_alpha)

    def test_compute_trim_tab_angle(self, wingsail_controller):
        """
        Tests the computation of trim tab angle.

        Args:
            wingsail_controller: Instance of WingsailController.
        """
        desired_alpha = 10.0
        apparent_wind_direction = 45.0
        expected_trim_tab_angle = 10.0
        computed_trim_tab_angle = wingsail_controller._compute_trim_tab_angle(
            desired_alpha, apparent_wind_direction)
        assert math.isclose(computed_trim_tab_angle, expected_trim_tab_angle)

    def test_get_trim_tab_angle(self, wingsail_controller):
        """
        Tests the computation of final trim tab angle.

        Args:
            wingsail_controller: Instance of WingsailController.
        """
        apparent_wind_speed = 1.0
        apparent_wind_direction = 45.0
        expected_trim_tab_angle = 5.75
        computed_trim_tab_angle = wingsail_controller.get_trim_tab_angle(
            apparent_wind_speed, apparent_wind_direction)
        assert math.isclose(computed_trim_tab_angle, expected_trim_tab_angle)
