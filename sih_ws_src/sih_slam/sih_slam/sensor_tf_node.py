import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


class SensorTFNode(Node):

    def __init__(self):
        super().__init__('sensor_tf_node')

        self.br = StaticTransformBroadcaster(self)

        transforms = [
            (0.35, 0.0, 3.05, 'base_link', 'lidar_link'),
            (1.20, 0.0, 3.20, 'base_link', 'front_camera_link'),
            (0.0,  0.0, 2.25, 'base_link', 'imu_link'),
            (-0.40, 0.0, 2.80, 'base_link', 'gps_link'),
        ]

        msgs = []

        for x, y, z, parent, child in transforms:
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = parent
            t.child_frame_id = child

            t.transform.translation.x = x
            t.transform.translation.y = y
            t.transform.translation.z = z

            t.transform.rotation.x = 0.0
            t.transform.rotation.y = 0.0
            t.transform.rotation.z = 0.0
            t.transform.rotation.w = 1.0

            msgs.append(t)

        self.br.sendTransform(msgs)

        self.get_logger().info(
            'Published static TF: base_link -> lidar/camera/imu/gps'
        )


def main(args=None):
    rclpy.init(args=args)
    node = SensorTFNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
