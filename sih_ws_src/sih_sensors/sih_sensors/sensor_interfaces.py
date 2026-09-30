#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, LaserScan, Imu, NavSatFix


class SensorInterfaces(Node):

    def __init__(self):
        super().__init__('sensor_interfaces')

        self.camera_pub = self.create_publisher(
            Image, '/camera/image_raw', 10)

        self.lidar_pub = self.create_publisher(
            LaserScan, '/scan', 10)

        self.imu_pub = self.create_publisher(
            Imu, '/imu/data', 10)

        self.gps_pub = self.create_publisher(
            NavSatFix, '/gps/fix', 10)

        self.timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('SIH Sensor Interfaces started')
        self.get_logger().info(
            'Camera: /camera/image_raw')
        self.get_logger().info(
            'LiDAR: /scan')
        self.get_logger().info(
            'IMU: /imu/data')
        self.get_logger().info(
            'GPS: /gps/fix')

    def publish_status(self):
        self.get_logger().info('Sensor interfaces ready')


def main(args=None):
    rclpy.init(args=args)

    node = SensorInterfaces()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
