import rclpy
from rclpy.node import Node
import math
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import tf_transformations

class DynamicFramePublisher(Node):
    def __init__(self):
        super().__init__('dynamic_tf2_publisher')
        self.br = TransformBroadcaster(self)
        self.timer = self.create_timer(0.05, self.broadcast_timer_callback)
        self.t0 =self.get_clock().now()

    def broadcast_timer_callback(self):
        now = self.get_clock().now()
        elapsed = (now - self.t0).nanoseconds / 1e9

        # simple cirular motion
        radius = 1.0
        omega = 0.5  # rad/s
        x = radius * math.cos(omega * elapsed)
        y = radius * math.sin(omega * elapsed)
        yaw = omega * elapsed + math.pi/2

        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'

        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = 0.0

        q = tf_transformations.quaternion_from_euler(0,0,yaw)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = DynamicFramePublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()