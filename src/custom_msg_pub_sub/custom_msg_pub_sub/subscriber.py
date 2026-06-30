import rclpy
from rclpy.node import Node

from custom_interfaces.msg import RobotStatus

# string robot_name
# float32 battery_level
# bool is_charging
# int32 error_code


topic = "robot_status"

class SubscribeStatus(Node):
    def __init__(self):
        super().__init__('robotStatusSubscriber')
        self.subscriber = self.create_subscription(
            RobotStatus,
            topic,
            self.my_callback_fun,
            5
        )

    def my_callback_fun(self, my_status):
        self.get_logger().info(
            f'Robot: {my_status.robot_name}, '
            f'Battery: {my_status.battery_level:.2f}%, '
            f'Charging: {my_status.is_charging}, '
            f'Error: {my_status.error_code} '
        )

def main(args=None):
    rclpy.init(args=args)

    subscriber_node = SubscribeStatus()

    rclpy.spin(subscriber_node)

    subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()