import rclpy
from rclpy.node import Node
from custom_interfaces.msg import RobotStatus

# string robot_name
# float32 battery_level
# bool is_charging
# int32 error_code


topic = "robot_status"

class PublishStatus(Node):
    def __init__(self):
        super().__init__('robotStatusPublisher')
        self.publisher = self.create_publisher(
            RobotStatus,
            topic,
            5
        )

        # period ofr publishing the message
        self.period = 1
        self.timer = self.create_timer(self.period, self.my_callback_fn)
        self.counter = 0
        self.charge = 100

    def my_callback_fn(self):
        my_status = RobotStatus()
        self.charge = self.charge - 0.05
        if self.charge < 0:
            self.charge = 100
        my_status.robot_name = "Sophus"
        my_status.battery_level = self.charge
        my_status.is_charging = False
        my_status.error_code = 404

        self.publisher.publish(my_status)
        self.get_logger().info(
            f'Robot: {my_status.robot_name}, '
            f'Battery: {my_status.battery_level:.2f}%, '
            f'Charging: {my_status.is_charging}, '
            f'Error: {my_status.error_code} '
            f'Counter: {self.counter}'
        )
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)

    # create a node
    custom_publisher = PublishStatus()

    # spin the node
    rclpy.spin(custom_publisher)
    custom_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


