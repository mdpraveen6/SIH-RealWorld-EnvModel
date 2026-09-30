#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from vision_msgs.msg import Detection2D, Detection2DArray

from ultralytics import YOLO


class YoloNode(Node):

    def __init__(self):
        super().__init__('yolo_node')

        self.bridge = CvBridge()

        self.get_logger().info('Loading YOLO11n model...')

        self.model = YOLO('yolo11n.pt')

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.detection_pub = self.create_publisher(
            Detection2DArray,
            '/perception/detections',
            10
        )

        self.get_logger().info('YOLO perception node started')
        self.get_logger().info('Input: /camera/image_raw')
        self.get_logger().info('Output: /perception/detections')

    def image_callback(self, msg):

        try:

            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

            results = self.model(
                frame,
                verbose=False
            )

            detection_msg = Detection2DArray()

            detection_msg.header = msg.header

            total = 0

            for result in results:

                if result.boxes is None:
                    continue

                for box in result.boxes:

                    detection = Detection2D()

                    xyxy = box.xyxy[0].tolist()

                    x1, y1, x2, y2 = xyxy

                    detection.bbox.center.position.x = (
                        (x1 + x2) / 2.0
                    )

                    detection.bbox.center.position.y = (
                        (y1 + y2) / 2.0
                    )

                    detection.bbox.size_x = x2 - x1
                    detection.bbox.size_y = y2 - y1

                    detection_msg.detections.append(
                        detection
                    )

                    total += 1

            self.detection_pub.publish(
                detection_msg
            )

            self.get_logger().info(
                f'Frame processed | Detections: {total}'
            )

        except Exception as e:

            self.get_logger().error(
                f'YOLO processing failed: {e}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = YoloNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
