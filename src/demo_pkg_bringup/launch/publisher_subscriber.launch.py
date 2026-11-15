#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    publisher_node = Node(
        package="demo_pkg",
        executable="py_publisher",
        name="demo_publisher"
    )

    subscriber_node = Node(
        package="demo_pkg",
        executable="py_subscriber",
        name="demo_subscriber"
    )

    ld.add_action(publisher_node)
    ld.add_action(subscriber_node)
    return ld