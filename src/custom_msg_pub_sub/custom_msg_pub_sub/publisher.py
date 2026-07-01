import rclpy
from rclpy.node import Node
from custom_interfaces.msg import RobotStatus
from rcl_interfaces.msg import SetParametersResult

# string robot_name
# float32 battery_level
# bool is_charging
# int32 error_code


topic = "robot_status"

class PublishStatus(Node):
    def __init__(self):
        super().__init__('robotStatusPublisher')

        # Declare the parameter
        self.declare_parameter('robot_name', "Sophus")
        self.declare_parameter('publish_period', 1.0)
        self.declare_parameter('initial_battery', 100.0)
        self.declare_parameter('drain_rate', 0.5)

        # Read the new parameter value
        self.robot_name = self.get_parameter('robot_name').value
        self.period = self.get_parameter('publish_period').value
        self.charge = self.get_parameter('initial_battery').value
        self.drain_rate = self.get_parameter('drain_rate').value

        self.publisher = self.create_publisher(
            RobotStatus,
            topic,
            5
        )

        self.timer = self.create_timer(self.period, self.my_callback_fn)
        self.counter = 0

        self.add_on_set_parameters_callback(self.on_param_change)  #to run every time someone calls ros2 param set on this node

    def on_param_change(self, params):
        for p in params:
            if p.name == 'robot_name':
                self.robot_name = p.value
                self.get_logger().info(f'robot_name updated -> "{self.robot_name}"')
            elif p.name == 'drain_rate':
                self.drain_rate = p.value
                self.get_logger().info(f'Drain rate updated -> "{self.drain_rate}"')
        return SetParametersResult(successful=True)
                

    def my_callback_fn(self):
        my_status = RobotStatus()
        self.charge = self.charge - self.drain_rate
        if self.charge < 0:
            self.charge = self.get_parameter("initial_battery").value

        my_status.robot_name = self.robot_name
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


