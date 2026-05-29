import rclpy
from rclpy.node import Node

# we will receive floats and strings
from std_msgs.msg import Float32
from std_msgs.msg import String

# topic for the float message
topic1 = 'float_topic'   # same as in the publisher
topic2 = 'string_topic'  # same as in the subscriber

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')

        self.sub_float = self.create_subscription(Float32, topic1, self.callback_fun1,10)

        self.sub_string = self.create_subscription(String, topic2, self.callback_fun2, 10)
    
    def callback_fun1(self,msg):
        self.get_logger().info('Float message: "%s"' % msg.data)
    
    def callback_fun2(self,msg):
        self.get_logger().info('String message: "%s"' %msg.data)

def main(args=None):
    rclpy.init(args=args)

    subscriber_node = SubscriberNode()

    rclpy.spin(subscriber_node)

    subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()