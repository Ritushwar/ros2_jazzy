import rclpy
from rclpy.node import Node
from tf2_ros import TransformException  # exception class that gets raised when a transform lookup fails
from tf2_ros.buffer import Buffer       # to store the published frame
from tf2_ros.transform_listener import TransformListener   # subscriber that listen and feed in the buffer

class FrameListener(Node):
    def __init__(self):
        super().__init__('tf2_frame_listener')

        # for static_broadcaster
        # self.target_frame = 'base_link'   
        # self.source_frame = 'camera_link' 

        # for dynamic broadcaster
        self.target_frame = 'odom'
        self.source_frame = 'base_link'




        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.timer = self.create_timer(0.05, self.on_timer)

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.source_frame,
                rclpy.time.Time()
            )

        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {self.source_frame} to {self.target_frame}: {ex}'
            )
            return
        self.get_logger().info(
            f'Translation: x={t.transform._translation.x:.2f}, '
            f'Translation: y={t.transform.translation.y:.2f}, '
            f'Translation: z={t.transform.translation.z:.2f}, '
        )

def main():
    rclpy.init()
    node = FrameListener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()
