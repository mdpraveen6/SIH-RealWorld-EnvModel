#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan


class LidarRelay(Node):

    def __init__(self):
        super().__init__('lidar_relay')

        self.sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.pub = self.create_publisher(
            LaserScan,
            '/scan_fixed',
            10
        )

        self.get_logger().info('LiDAR relay started')
        self.get_logger().info('Input: /scan')
        self.get_logger().info('Output: /scan_fixed')
        self.get_logger().info('Frame: lidar_link')

    def scan_callback(self, msg):

        msg.header.frame_id = 'lidar_link'

        self.pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = LidarRelay()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
