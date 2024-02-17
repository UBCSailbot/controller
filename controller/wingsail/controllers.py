from controller.common.constants import CHORD_WIDTH_MAIN_SAIL, KINEMATIC_VISCOSITY
from controller.common.lut import LUT


class WingsailController:
    def __init__(self):
        self.lut = LUT()  # Placeholder for the LUT class

    def _compute_reynolds_number(self, apparent_wind_speed):
        """
        Computes the Reynolds number for the main sail.

        Parameters:
        - apparent_wind_speed (float): The apparent wind speed in meters per second.

        Returns:
        - reynolds_number (float): The computed Reynolds number for the main sail.
        """
        reynolds_number = (apparent_wind_speed * CHORD_WIDTH_MAIN_SAIL) / KINEMATIC_VISCOSITY
        return reynolds_number

    def _compute_angle_of_attack(self, reynolds_number, look_up_table):
        """
        Computes the desired angle of attack based on Reynolds number and a lookup table.

        Parameters:
        - reynolds_number (float): The Reynolds number.
        - look_up_table: A 2D numpy array containing Reynolds numbers in the first column
          and corresponding desired angles of attack in the second column.

        Returns:
        - desired_alpha (float): The computed desired angle of attack based on the provided
          Reynolds number and lookup table.
        """
        desired_alpha = self.lut.interpolate(reynolds_number, look_up_table)
        return desired_alpha

    def _compute_trim_tab_angle(self, desired_alpha, apparent_wind_direction):
        """
        Range: -180 < direction <= 180 for symmetry

        Parameters:
        - desired_alpha (float): The desired angle of attack.
        - apparent_wind_direction (float): The apparent wind direction in degrees.

        Returns:
        - trim_tab_angle (float): The computed trim tab angle based on the provided desired angle
          of attack, apparent wind direction, and boat direction.

        """
        if apparent_wind_direction >= 0:
            trim_tab_angle = desired_alpha
        else:
            trim_tab_angle = -desired_alpha

        return trim_tab_angle

    def get_trim_tab_angle(self, apparent_wind_speed, apparent_wind_direction):
        """
        Computes and returns the final trim tab angle.

        Range: -180 < direction <= 180 for symmetry

        Parameters:
        - apparent_wind_speed (float): The apparent wind speed in meters per second.
        - apparent_wind_direction (float): The apparent wind direction in degrees.

        Returns:
        - trim_tab_angle (float): The computed trim tab angle.
        """
        reynolds_number = self._compute_reynolds_number(apparent_wind_speed)
        desired_alpha = self._compute_angle_of_attack(reynolds_number, self.lut.get_table())
        trim_tab_angle = self._compute_trim_tab_angle(desired_alpha, apparent_wind_direction)

        return trim_tab_angle
