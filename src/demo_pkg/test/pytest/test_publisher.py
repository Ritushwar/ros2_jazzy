"""
Test suite for the ROS2 publisher node
This script contains the unit tests for verifying the functionality of ROS2 publisher.
It tests the node creation, message counter increment and message content formatting

--------------------------
Subscription Topics
    1) String
    2) Float

---------------------------
Publishing Topics
    1) String
    2) Float

Author: Ritushwar Neupane
Date: Thu May 28, 2026
"""

import pytest
import rclpy
from std_msgs.msg import String
from std_msgs.msg import Float32

from demo_pkg.publisher_python import PublisherNode

def test_publisher_creation():
    """
    Test if the publisher node is correctly created
    This test verifies:
    1) The node name is set correctly
    2) The publisher object exists
    3) The topics name is correct

    :raises: AssertionError if any of the checks fails
    """
    # Initialize ROS2 communication
    rclpy.init()

    try:
        # create an instance of publisher node
        node = PublisherNode()

        # Test1: Verify the node has the expected name
        assert node.get_name() == "publisher_node"

        # Test2: Verify the publisher exists
        assert hasattr(node, 'pub_float')
        assert hasattr(node, 'pub_string')

        # Test3: Verify the node has the correct topics name
        assert node.pub_float.topic_name == '/float_topic'
        assert node.pub_string.topic_name == '/string_topic'

    finally:
        # clean up ros communication
        node.destroy_node()
        rclpy.shutdown()

def test_message_counter():
    """
    Test if the message counter increment correctly
    This test verify that the counter increases by 1
    """

    # Initialize the ROS2 communication
    rclpy.init()

    try:
        node = PublisherNode()
        initial_count = node.counter
        node.callback_fun()
        assert node.counter == initial_count + 1
    finally:
        node.destroy_node()
        rclpy.shutdown()

def test_message_value():
    """
    Test if the message value increment correctly
    This test verify that the counter increases by 0.01
    """

    # Initialize the ROS2 communication
    rclpy.init()

    try:
        node = PublisherNode()
        initial_value = node.value
        node.callback_fun()
        assert abs(node.value - (initial_value + 0.01)) < 1e-6

    finally:
        node.destroy_node()
        rclpy.shutdown()

def test_message_content():
    """
    Test if the message content is formatted correctly

    This test verifies that the message string is properly formatted using an f -string
    with the current counter value

    : raises : AssertionError if the message format doesn't match the expected output
    """

    rclpy.init()

    try:
        node = PublisherNode()

        # set the counter to a known value for testing
        node.counter = 5

        # Expected Message
        expected_message = 'Message number: 5'

        # Actual Message
        actual_message = 'Message number: %d' % node.counter
        assert expected_message == actual_message

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    pytest.main(['-v'])
