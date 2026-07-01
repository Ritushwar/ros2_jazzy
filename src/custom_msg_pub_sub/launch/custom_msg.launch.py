import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('custom_msg_pub_sub')
    params_file = os.path.join(pkg_share, 'config', 'params.yaml')
    publisher_node = Node(
        package='custom_msg_pub_sub',
        executable='publisher',
        name='robotStatusPublisher',
        # parameters=[{
        #     'robot_name': 'Sophus',
        #     'publish_period': 1.0,
        #     'initial_battery': 100.0,
        #     'drain_rate': 0.05,
        # }],
        parameters=[params_file],
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
