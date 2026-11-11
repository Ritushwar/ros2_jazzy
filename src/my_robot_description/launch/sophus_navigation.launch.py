from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 1. Gazebo simulation
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('my_robot_description'),
                'launch',
                'sophus_lidar_gazebo.launch.py'
            ])
        )
    )

    # 2. RViz visualization
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('my_robot_description'),
                'launch',
                'sophus_nav2.launch.py'
            ])
        )
    )

    return LaunchDescription([
        gazebo,
        nav2
    ])