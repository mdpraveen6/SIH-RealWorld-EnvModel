#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster


class OdomNode(Node):

    def __init__(self):
        super().__init__('odom_node')

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.last_time = self.get_clock().now()

        self.cmd_sub = self.create_subscription(
            Twist,
            '/sih_ugv/cmd_vel',
            self.cmd_callback,
            10
        )

        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(
            0.02,
            self.update
        )

        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

        self.get_logger().info('SIH Odometry Node started')
        self.get_logger().info('Input: /cmd_vel')
        self.get_logger().info('Output: /odom')
        self.get_logger().info('TF: odom -> base_link')

    def cmd_callback(self, msg):

        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

    def update(self):

        now = self.get_clock().now()

        dt = (
            now - self.last_time
        ).nanoseconds / 1e9

        self.last_time = now

        if dt <= 0.0 or dt > 1.0:
            return

        self.x += (
            self.linear_velocity *
            math.cos(self.yaw) *
            dt
        )

        self.y += (
            self.linear_velocity *
            math.sin(self.yaw) *
            dt
        )

        self.yaw += (
            self.angular_velocity * dt
        )

        odom = Odometry()

        odom.header.stamp = now.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y

        odom.pose.pose.orientation.z = math.sin(
            self.yaw / 2.0
        )

        odom.pose.pose.orientation.w = math.cos(
            self.yaw / 2.0
        )

        odom.twist.twist.linear.x = self.linear_velocity
        odom.twist.twist.angular.z = self.angular_velocity

        self.odom_pub.publish(odom)

        tf = TransformStamped()

        tf.header.stamp = now.to_msg()
        tf.header.frame_id = 'odom'
        tf.child_frame_id = 'base_link'

        tf.transform.translation.x = self.x
        tf.transform.translation.y = self.y

        tf.transform.rotation.z = math.sin(
            self.yaw / 2.0
        )

        tf.transform.rotation.w = math.cos(
            self.yaw / 2.0
        )

        self.tf_broadcaster.sendTransform(tf)


def main(args=None):

    rclpy.init(args=args)

    node = OdomNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
