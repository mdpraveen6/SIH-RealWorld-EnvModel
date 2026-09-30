#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, LaserScan, Imu, NavSatFix
from builtin_interfaces.msg import Time


class SensorServer(Node):

    def __init__(self):
        super().__init__('sensor_server')

        # ============================================================
        # SERVER OUTPUTS
        # ============================================================
        self.camera_pub = self.create_publisher(
            Image, '/sih_ugv/sensors/camera', 10)

        self.lidar_pub = self.create_publisher(
            LaserScan, '/sih_ugv/sensors/lidar', 10)

        self.imu_pub = self.create_publisher(
            Imu, '/sih_ugv/sensors/imu', 10)

        self.gps_pub = self.create_publisher(
            NavSatFix, '/sih_ugv/sensors/gps', 10)

        # 10 Hz master sensor server
        self.timer = self.create_timer(0.1, self.publish_sensors)

        self.counter = 0

        self.get_logger().info('======================================')
        self.get_logger().info('SIH SENSOR SERVER')
        self.get_logger().info('SYNTHETIC SENSOR MODE')
        self.get_logger().info('Camera + LiDAR + IMU + GPS')
        self.get_logger().info('Gazebo SDF files NOT modified')
        self.get_logger().info('======================================')

    def stamp(self):
        return self.get_clock().now().to_msg()

    # ============================================================
    # LIDAR
    # ============================================================
    def publish_lidar(self, stamp):

        msg = LaserScan()

        msg.header.stamp = stamp
        msg.header.frame_id = 'lidar_link'

        msg.angle_min = -math.pi
        msg.angle_max = math.pi
        msg.angle_increment = math.radians(0.5)

        msg.time_increment = 0.0
        msg.scan_time = 0.1

        msg.range_min = 0.2
        msg.range_max = 80.0

        samples = 720

        # Synthetic environment:
        # forward obstacle at ~10 m,
        # side obstacles at different distances.
        ranges = []

        for i in range(samples):

            angle = msg.angle_min + i * msg.angle_increment

            distance = 30.0

            # Front obstacle
            if abs(angle) < math.radians(12):
                distance = 10.0

            # Left obstacle
            if abs(angle - math.pi / 2) < math.radians(8):
                distance = 6.0

            # Right obstacle
            if abs(angle + math.pi / 2) < math.radians(8):
                distance = 8.0

            ranges.append(float(distance))

        msg.ranges = ranges

        self.lidar_pub.publish(msg)

    # ============================================================
    # IMU
    # ============================================================
    def publish_imu(self, stamp):

        msg = Imu()

        msg.header.stamp = stamp
        msg.header.frame_id = 'imu_link'

        msg.orientation.w = 1.0

        msg.angular_velocity.x = 0.0
        msg.angular_velocity.y = 0.0
        msg.angular_velocity.z = 0.0

        msg.linear_acceleration.x = 0.0
        msg.linear_acceleration.y = 0.0
        msg.linear_acceleration.z = 9.81

        self.imu_pub.publish(msg)

    # ============================================================
    # GPS
    # ============================================================
    def publish_gps(self, stamp):

        msg = NavSatFix()

        msg.header.stamp = stamp
        msg.header.frame_id = 'gps_link'

        # Example Baylands test position
        msg.latitude = 37.4149
        msg.longitude = -121.9489
        msg.altitude = 5.0

        self.gps_pub.publish(msg)

    # ============================================================
    # CAMERA
    # ============================================================
    def publish_camera(self, stamp):

        msg = Image()

        msg.header.stamp = stamp
        msg.header.frame_id = 'front_camera_link'

        msg.height = 360
        msg.width = 640

        msg.encoding = 'rgb8'
        msg.is_bigendian = 0

        msg.step = msg.width * 3

        # Gray synthetic camera frame.
        # Avoids requiring cv2/numpy.
        pixel = bytes([80, 80, 80])

        msg.data = pixel * (msg.width * msg.height)

        msg.data = bytes(msg.data)

        self.camera_pub.publish(msg)

    # ============================================================
    # MASTER SENSOR LOOP
    # ============================================================
    def publish_sensors(self):

        stamp = self.stamp()

        self.publish_lidar(stamp)
        self.publish_imu(stamp)
        self.publish_gps(stamp)
        self.publish_camera(stamp)

        self.counter += 1

        if self.counter % 50 == 0:
            self.get_logger().info(
                'Sensor server streaming | '
                'Camera 10Hz | LiDAR 10Hz | IMU 10Hz | GPS 10Hz'
            )


def main(args=None):

    rclpy.init(args=args)

    node = SensorServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()

        node.destroy_node()


if __name__ == '__main__':
    main()
