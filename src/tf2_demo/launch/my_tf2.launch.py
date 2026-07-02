import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('tf2_demo')
    # params_file = os.path.join(pkg_share, 'config', 'params.yaml')
    publisher_node = Node(
        package='tf2_demo',
        executable='tf_broadcaster',
        name='static_tf2_broadcaster',
        output='screen',
    )
    dynamic_publisher_node = Node(
        package='tf2_demo',
        executable='dynamic_broadcaster',
        name='dynamic_tf2_publisher',
        output='screen',

    )

    subscriber_node = Node(
        package='tf2_demo',
        executable='tf_listener',
        name='tf2_frame_listener',
        output='screen',
    )

    return LaunchDescription([
        dynamic_publisher_node,
        subscriber_node,
    ])
