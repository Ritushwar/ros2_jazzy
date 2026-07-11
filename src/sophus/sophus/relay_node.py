import cv2
import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge

received_topic = "/image_raw/compressed"
publish_topic = "image_raw"

class ImageRelay(Node):
    def __init__(self):
        super().__init__('image_realy')
        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            CompressedImage,
            received_topic,
            self.image_callback,
            qos_profile_sensor_data
        )

        self.publisher = self.create_publisher(
            Image,
            publish_topic,
            qos_profile_sensor_data
        )
        self.get_logger().info("Image relay node started")

    def image_callback(self, msg):
        try:
            # convert bytes to numpy array
            np_arry = np.frombuffer(msg.data, np.uint8)

            # decode JPEG
            frame = cv2.imdecode(np_arry, cv2.IMREAD_COLOR)

            if frame is None:
                self.get_logger().warning("Failed to decode image")
                return
            
            # convert opencv to ROS image
            image_msg = self.bridge.cv2_to_imgmsg(
                frame,
                encoding='bgr8'
            )

            # add time stamp and frame if
            image_msg.header = msg.header

            self.publisher.publish(image_msg)
        
        except Exception as e:
             self.get_logger().error(f"Relay error: {e}")

def main(args=None):
    rclpy.init(args=args)
    realy_node = ImageRelay()
    rclpy.spin(realy_node)

    realy_node.destroy_node()
    rclpy.shutdown()

if __name__ == "main":
    main()