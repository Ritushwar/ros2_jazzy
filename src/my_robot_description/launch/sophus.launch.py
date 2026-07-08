import os
import xacro
from ament_index_python.packages import get_package_share_directory  # finds where a ROS 2 package is installed
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = get_package_share_directory('my_robot_description')
    xacro_file = os.path.join(pkg_path, 'urdf', 'sophus.urdf.xacro')

    robot_description_config = xacro.process_file(xacro_file)

    robot_description = {
        "robot_description": robot_description_config.toxml()
    }

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2'
        ),
     ]
    )