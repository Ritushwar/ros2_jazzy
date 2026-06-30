import sys
import rclpy
from rclpy.node import Node
from custom_interfaces.srv import AddTwoInt
cl1 = 'add_two_int'

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_int_client')
        self.client = self.create_client(
            AddTwoInt,
            cl1,
        )
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for response...")

    def send_request(self,a,b):
        req = AddTwoInt.Request()
        req.a = a
        req.b = b
        future_response = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future=future_response)
        return future_response.result()

def main():
    rclpy.init()
    my_node = AddTwoIntsClient()
    response = my_node.send_request(int(sys.argv[1]), int(sys.argv[2]))
    my_node.get_logger().info(f'Response: {response.sum}')
    my_node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()
