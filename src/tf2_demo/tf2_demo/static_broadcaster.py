import sys
import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
import tf_transformations

class staticFramePublisher(Node):
    def __init__(self):
        super().__init__('static_tf2_broadcaster')
        self.br = StaticTransformBroadcaster(self)  # creates an object capable of publishing static transforms
        self.make_transform()    # calling the function

    def make_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'camera_link'

        # translation(meters)
        t.transform.translation.x = 0.1
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.2

        # rotation (roll- pitch, yaw -> quaternion)
        q = tf_transformations.quaternion_from_euler(0,0,0)
        t.transform.translation.x = q[0]
        t.transform.translation.y = q[1]
        t.transform.translation.z = q[2]
        # t.transform.translation.w = q[3]

        self.br.sendTransform(t)
        self.get_logger().info('Static transform base_link -> camera_frame published')

def main():
    rclpy.init()
    node = staticFramePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
