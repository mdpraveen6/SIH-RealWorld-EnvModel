import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdVelRelay(Node):
    def __init__(self):
        super().__init__('cmd_vel_relay')

        self.publisher = self.create_publisher(
            Twist,
            '/sih_ugv/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel_smoothed',
            self.cmd_callback,
            10
        )

        self.get_logger().info(
            'Nav2 → UGV command relay started'
        )

    def cmd_callback(self, msg):
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
