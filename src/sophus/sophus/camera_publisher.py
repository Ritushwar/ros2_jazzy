import cv2
import rclpy
import threading
import numpy as np
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data


from sensor_msgs.msg import CompressedImage, CameraInfo
from cv_bridge import CvBridge
topic = '/image_raw/compressed'
info_topic = '/camera_info'

class CamPublisher(Node):
    def __init__(self):
        super().__init__('cam_publisher')
        self.bridge = CvBridge()

        self.publisher = self.create_publisher(
            CompressedImage,        #data_types
            topic,                  # topic
            qos_profile_sensor_data
        )

        self.info_publisher = self.create_publisher(
            CameraInfo,
            info_topic,
            qos_profile_sensor_data
        )
        
        url = "http://192.168.31.109:8080/video"
        self.cap = cv2.VideoCapture(url)
        if not self.cap.isOpened():
            self.get_logger().error("Cannot connect to droid cam")
            return
        else:
            self.get_logger().info("Camera Connected")

        # shared latest-frame state
        self.latest_frame = None
        self.frame_lock = threading.Lock()
        self.running = True

        # background thread: reads as fast as the network allows,

        # never blocks the ROS publish timer
        self.capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.capture_thread.start()
        self.timer = self.create_timer(0.03,self.publish_frame)

    def capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self.get_logger().warning("Frame not received", throttle_duration_sec=2.0)
                continue
            with self.frame_lock:
                self.latest_frame = frame

    def build_camera_info(self, width, height, stamp):
        info = CameraInfo()
        info.header.stamp = stamp
        info.header.frame_id='camera'
        info.width = width
        info.height = height

        info.distortion_model = "plumb_bob"
        info.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        info.k = [float(width), 0.0, width / 2.0,
                  0.0, float(width), height / 2.0,
                  0.0, 0.0, 1.0]
        info.r = [1.0, 0.0, 0.0,
                  0.0, 1.0, 0.0,
                  0.0, 0.0, 1.0]
        info.p = [float(width), 0.0, width / 2.0, 0.0,
                  0.0, float(width), height / 2.0, 0.0,
                  0.0, 0.0, 1.0, 0.0]
        return info

    def publish_frame(self):
        with self.frame_lock:
            frame = self.latest_frame

        if frame is None:
            return
        
        # Compress to JPEG (Quality 80)
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        if not ret:
            return

        stamp = self.get_clock().now().to_msg()
        msg = CompressedImage()
        msg.header.stamp = stamp
        msg.header.frame_id = "camera"
        msg.format = "jpeg"
        msg.data = buffer.tobytes()
        self.publisher.publish(msg)

        height, width = frame.shape[:2]
        info_msg = self.build_camera_info(width, height, stamp)
        self.info_publisher.publish(info_msg)

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    cam_node = CamPublisher()
    rclpy.spin(cam_node)
    cam_node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()