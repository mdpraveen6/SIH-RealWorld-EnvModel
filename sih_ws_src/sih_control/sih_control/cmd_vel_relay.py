import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdVelRelay(Node):
    def __init__(self):
        super().__init__('cmd_vel_relay')

        self.pub = self.create_publisher(
            Twist,
            '/sih_ugv/cmd_vel',
            10
        )

        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel_nav',
            self.callback,
            10
        )

        self.get_logger().info(
            'CMD VEL RELAY: /cmd_vel_nav -> /sih_ugv/cmd_vel'
        )

    def callback(self, msg):
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelRelay()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
