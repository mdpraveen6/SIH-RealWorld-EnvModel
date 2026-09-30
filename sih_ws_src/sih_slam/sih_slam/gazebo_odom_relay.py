import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class GazeboOdomRelay(Node):
    def __init__(self):
        super().__init__('gazebo_odom_relay')

        self.publisher = self.create_publisher(
            Odometry, '/odom', 10)

        self.tf_broadcaster = TransformBroadcaster(self)

        self.subscription = self.create_subscription(
            Odometry,
            '/sih_ugv/ackermann_odometry',
            self.odom_callback,
            10)

        self.get_logger().info('Gazebo odometry relay started')
        self.get_logger().info('SYSTEM TIME relay enabled')

    def odom_callback(self, msg):
        now = self.get_clock().now().to_msg()

        msg.header.stamp = now
        msg.header.frame_id = 'odom'
        msg.child_frame_id = 'base_link'

        self.publisher.publish(msg)

        tf = TransformStamped()
        tf.header.stamp = now
        tf.header.frame_id = 'odom'
        tf.child_frame_id = 'base_link'

        tf.transform.translation.x = msg.pose.pose.position.x
        tf.transform.translation.y = msg.pose.pose.position.y
        tf.transform.translation.z = msg.pose.pose.position.z
        tf.transform.rotation = msg.pose.pose.orientation

        self.tf_broadcaster.sendTransform(tf)


def main(args=None):
    rclpy.init(args=args)
    node = GazeboOdomRelay()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
