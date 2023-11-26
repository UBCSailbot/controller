#!/usr/bin/env python3

"""The ROS node for the wingsail controller."""

import rclpy
import rclpy.utilities
from custom_interfaces.msg import GPS, WindSensor
from rclpy.node import Node


def main(args=None):
    rclpy.init(args=args)
    node = WingsailControllerNode()
    rclpy.spin(node=node)
    node.destroy_node()
    rclpy.shutdown()


class WingsailControllerNode(Node):
    """
    A ROS node that controls the trim tab angle wingsail of the boat. The objective
    of the wingsail controller is to maintain the wingsail at a desired angle of attack
    while optimizing for speed by maximizing the lift-to-drag ratio of the wingsail.

    Subscriptions:
        __filtered_wind_sensors_sub (Subscription): Subscribes to a `WindSensor` message.
        __gps_sub (Subscription): Subscribes to a 'GPS' message.

    Publishers:
        TO BE ADDED
    """

    def __init__(self):
        """Initializes an instance of this class."""
        super().__init__("wingsail_ctrl_node")

        self.get_logger().debug("Initializing node...")
        self.__init_private_attributes()
        self.__declare_ros_parameters()
        self.__init_subscriptions()
        self.__init_publishers()
        self.get_logger().debug("Node initialization complete. Starting execution...")

    def __init_private_attributes(self):
        """Initializes private attributes of this class that are not initialized anywhere else
        during the initialization process.
        """
        self.__trim_tab_angle = 0.0
        self.filtered_wind_sensor = None
        self.gps = None

    def __declare_ros_parameters(self):
        """Declares ROS parameters from the global configuration file that will be used in this
        node. This node will monitor for any changes to these parameters during execution and will
        update itself accordingly.
        """
        # TODO Update global YAML file with more configuration parameters and declare them here
        self.get_logger().debug("Declaring ROS parameters...")
        self.declare_parameters(
            namespace="",
            parameters=[
                ("pub_period_sec", rclpy.Parameter.Type.DOUBLE),
            ],
        )

        # TODO Revisit this debug statement. It might get ugly for args with complicated structures
        all_parameters = self._parameters
        for name, parameter in all_parameters.items():
            value_str = str(parameter.value)
            self.get_logger().debug(f"Got parameter {name} with value {value_str}")

    def __init_subscriptions(self):
        """Initializes the subscriptions of this node. Subscriptions pull data from other ROS
        topics for further usage in this node. Data is pulled from subscriptions periodically via
        callbacks, which are registered upon subscription initialization.
        """
        # TODO Implement this function by subscribing to topics that give the desired input data
        # Callbacks for each subscriptions should be defined as private methods of this class
        self.get_logger().debug("Initializing subscriptions...")

        self.__filtered_wind_sensor_sub = self.create_subscription(
            msg_type=WindSensor,
            topic="filtered_wind_sensor",
            callback=self.__filtered_wind_sensor_sub_callback,
            qos_profile=1,
        )

        self.__gps_sub = self.create_subscription(
            msg_type=GPS,
            topic="gps",
            callback=self.__gps_sub_callback,
            qos_profile=1,
        )

    def __init_publishers(self):
        """Initializes the publishers of this node. Publishers update ROS topics so that other ROS
        nodes in the system can utilize the data produced by this node.
        """
        # TODO Implement this function by initializing publishers for topics that give the desired
        # output data

        pass

    @property
    def pub_period(self) -> float:
        return self.get_parameter("pub_period_sec").get_parameter_value().double_value

    @property
    def trim_tab_angle(self) -> float:
        return self.__trim_tab_angle

    def __filtered_wind_sensor_sub_callback(self, msg):
        self.filtered_wind_sensor = msg
        self.get_logger().info(f"Received data from {self.__filtered_wind_sensor_sub.topic}")

    def __gps_sub_callback(self, msg):
        self.gps = msg
        self.get_logger().info(f"Received data from {self.__gps_sub.topic}")


if __name__ == "__main__":
    main()
