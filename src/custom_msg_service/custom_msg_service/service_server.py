import rclpy
from rclpy.node import Node
from custom_interfaces.srv import AddTwoInt
srv1 = 'add_two_int'

class AddTwoIntServer(Node):
    def __init__(self):
        super().__init__("add_two_int_server")
        self.server = self.create_service(
            AddTwoInt,
            srv1,
            self.my_call_back_fun
        )
        self.get_logger().info("Add Service Server Ready")

    def my_call_back_fun(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Incoming response:{request.a} + {request.b} = {response.sum}'
        )
        return response
    
def main():
    rclpy.init()
    my_node = AddTwoIntServer()
    rclpy.spin(my_node)
    my_node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()

