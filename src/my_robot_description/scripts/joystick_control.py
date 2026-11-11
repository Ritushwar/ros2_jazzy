#!/usr/bin/env python3
import socket
import struct
import time
import rclpy
from rclpy.node import Node

# /cmd_vel use the geometry_msgs/msg/Twist
from geometry_msgs.msg import Twist

#topic for the diff_drive
topic = "/cmd_vel"

# UDP Configuration
UDP_IP = "0.0.0.0"
UDP_PORT = 8000

# Joystick thresholds
LOW_THRESHOLD = 900
HIGH_THRESHOLD = 2700

# Velocity values
LINEAR_SPEED = 0.5
ANGULAR_SPEED = 1.0

class Velocity_Publisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher_node')

        # we have only one publiher
        self.my_pub = self.create_publisher(Twist, topic, 10)

        # Create UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

        # Non-blocking Socket
        self.sock.setblocking(False)

        # Joystick Value
        self.value_x = 1800
        self.value_y = 1800
        self.value_z = 1

        self.last_received_time = 0.0

        # Stop command if UDP data is lost
        self.timeout = 0.5

        # ROS 2 timer (50 Hz)
        self.period = 0.02

        self.timer = self.create_timer(self.period,self.callback_fun)

        self.get_logger().info("JoyStick receiver started....")

        self.get_logger().info(f"Publishing velocity on {topic}")

    def receive_udp(self):
        # first receive all the availabe packets
        # keep the latest valid reading

        while True:
            try:
                data, address = self.sock.recvfrom(1024)
            
            except BlockingIOError:
                break

            # check packet size
            if len(data) != 12:
                self.get_logger().warning(
                    f"Invalid packet size: {len(data)}"
                )
                continue

            # decode the value
            x, y, z = struct.unpack('<iii', data)

            # Validate joystick values
            if not (0 <= x <= 4095 and 0 <= y <= 4095):
                self.get_logger().warning(
                    "Invalid analog joystick values"
                )
                continue

            if z not in(1,0):
                continue


            # update the latest value
            self.value_x = x
            self.value_y = y
            self.value_z = z

            self.last_received_time = time.monotonic()

    def calculate_velocity(self):
        # initial velocity
        linear_x = 0.0
        angular_z = 0.0

        # joystick position
        x_left = self.value_x > HIGH_THRESHOLD
        x_right = self.value_x < LOW_THRESHOLD
        x_center = HIGH_THRESHOLD > self.value_x > LOW_THRESHOLD

        y_up = self.value_y > HIGH_THRESHOLD
        y_down = self.value_y < LOW_THRESHOLD
        y_center = HIGH_THRESHOLD > self.value_y > LOW_THRESHOLD

        if x_center & y_center:
            linear_x = 0.0
            angular_z = 0.0
        
        elif x_center & y_up:
            linear_x = 0.0
            angular_z = -1.0
        
        elif x_center & y_down:
            linear_x = 0.0
            angular_z = 1.0

        elif y_center & x_left:
            linear_x = 0.5
            angular_z = 0.0

        elif y_center & x_right:
            linear_x = -0.5
            angular_z = 0.0

        elif y_up & x_right:
            linear_x = -0.5
            angular_z = 1.0

        elif y_up & x_left:
            linear_x = 0.5
            angular_z = -1.0
        
        elif y_down & x_right:
            linear_x = -0.5
            angular_z = -1.0

        elif y_down & x_left:
            linear_x = 0.5
            angular_z = 1.0

        return linear_x, angular_z
    
    def callback_fun(self):
        # receive joystick data
        self.receive_udp()
        msg = Twist()

        current_time = time.monotonic()
        if (
            self.last_received_time == 0.0
            or current_time - self.last_received_time > self.timeout
        ):
            # Stop robot if communication is lost
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        else:
            # Calculate velocity
            linear_x, angular_z = self.calculate_velocity()

            msg.linear.x = linear_x
            msg.angular.z = angular_z

        self.my_pub.publish(msg)

        #  # Display joystick values
        # self.get_logger().info(
        #     f"X: {self.value_x} | "
        #     f"Y: {self.value_y} | "
        #     f"Z: {self.value_z} | "
        #     f"Linear X: {msg.linear.x:.2f} | "
        #     f"Angular Z: {msg.angular.z:.2f}",
        #     throttle_duration_sec=0.2
        # )

    def destroy_node(self):

        # Publish stop command before shutdown
        stop_msg = Twist()
        self.my_pub.publish(stop_msg)

        self.sock.close()

        super().destroy_node()

def main(args=None):

    rclpy.init(args=args)

    node = Velocity_Publisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Joystick receiver stopped.")

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()


        