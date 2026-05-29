import rclpy  # rclpy provide the standard API

# Node class - the parent class for building
from rclpy.node import Node

#we will send string and floats
from std_msgs.msg import Float32
from std_msgs.msg import String

#topic for the float message
topic1 = "float_topic"
topic2 = "string_topic"

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')

        # We have two publisher
        # publisher for the float
        self.pub_float = self.create_publisher(Float32, topic1, 10)  # datatype , topic, queue
    
        # publisher for the string
        self.pub_string = self.create_publisher(String, topic2, 10)

        # period for publishing message
        self.period = 1    # 1 sec
        self.timer = self.create_timer(self.period, self.callback_fun)

        # message counter
        self.counter = 0
        # float value
        self.value = 0
    
    def callback_fun(self):
        message1 = Float32()
        message2 = String()

        self.value = self.value + 0.01
        message1.data = self.value
        message2.data = 'Message number: %d' % self.counter

        self.pub_string.publish(message2)
        self.pub_float.publish(message1)

        self.get_logger().info('Publishing: "%s" and value %s' %(message2.data, message1.data))
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)

    # create node
    publisher_node = PublisherNode()

    # spin the node
    rclpy.spin(publisher_node)

    publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
