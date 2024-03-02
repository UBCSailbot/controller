import math

from controller.common.lut import LUT


class WingsailController:
    def __init__(self, chord_width_main_sail: float, kinematic_viscosity: float, lut: LUT) -> None:
        self.chord_width_main_sail = chord_width_main_sail
        self.kinematic_viscosity = kinematic_viscosity
        self.lut: LUT = lut

    def _compute_reynolds_number(self, apparent_wind_speed: float) -> float:
        """
        Computes the Reynolds number for the main sail.

        Args:
        - apparent_wind_speed (float): The apparent wind speed in meters per second.

        Returns:
        - reynolds_number (float): The computed Reynolds number for the main sail.
        """
        reynolds_number: float = (
            apparent_wind_speed * self.chord_width_main_sail
        ) / self.kinematic_viscosity
        return reynolds_number

    def _compute_angle_of_attack(self, reynolds_number: float, look_up_table: LUT) -> float:
        """
        Computes the desired angle of attack based on Reynolds number and a lookup table.

        Args:
        - reynolds_number (float): The Reynolds number.
        - look_up_table: A 2D numpy array containing Reynolds numbers in the first column
          and corresponding desired angles of attack in the second column.

        Returns:
        - desired_alpha (float): The computed desired angle of attack based on the provided
          Reynolds number and lookup table.
        """
        desired_alpha: float = self.lut(reynolds_number)  # Using __call__ method
        return desired_alpha

    def _compute_trim_tab_angle(
        self, desired_alpha: float, apparent_wind_direction: float
    ) -> float:
        """
        Range: -180 < direction <= 180 for symmetry

        Args:
        - desired_alpha (float): The desired angle of attack.
        - apparent_wind_direction (float): The apparent wind direction in degrees.

        Returns:
        - trim_tab_angle (float): The computed trim tab angle based on the provided desired angle
          of attack, apparent wind direction, and boat direction.

        """
        return math.copysign(desired_alpha, apparent_wind_direction)

    def get_trim_tab_angle(
        self, apparent_wind_speed: float, apparent_wind_direction: float
    ) -> float:
        """
        Computes and returns the final trim tab angle.

        Range: -180 < direction <= 180 for symmetry

        Args:
        - apparent_wind_speed (float): The apparent wind speed in meters per second.
        - apparent_wind_direction (float): The apparent wind direction in degrees.

        Returns:
        - trim_tab_angle (float): The computed trim tab angle.
        """
        reynolds_number: float = self._compute_reynolds_number(apparent_wind_speed)
        desired_alpha: float = self._compute_angle_of_attack(reynolds_number, self.lut)
        trim_tab_angle: float = self._compute_trim_tab_angle(
            desired_alpha, apparent_wind_direction
        )

        return trim_tab_angle
