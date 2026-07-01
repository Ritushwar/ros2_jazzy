from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    publisher_node = Node(
        package='custom_msg_pub_sub',
        executable='publisher',
        name='robotStatusPublisher',
        parameters=[{
            'robot_name': 'Sophus',
            'publish_period': 1.0,
            'initial_battery': 100.0,
            'drain_rate': 0.05,
        }],
        output='screen',
    )

    subscriber_node = Node(
        package='custom_msg_pub_sub',
        executable='subscriber',
        name='robotStatusPublisher',
        output='screen',
    )

    return LaunchDescription([
        publisher_node,
        subscriber_node,
    ])
