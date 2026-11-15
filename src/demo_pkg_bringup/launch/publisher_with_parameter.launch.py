#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    cpp_publisher_node = Node(
        package="demo_pkg",
        executable="para_publisher",
        name="param_publisher",
        parameters=[{"robot_name": "BUJJI"}]
    )


    ld.add_action(cpp_publisher_node)
    return ld