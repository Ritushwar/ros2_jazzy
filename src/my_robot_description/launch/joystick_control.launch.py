from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    joystick_node = Node(
        package='my_robot_description',
        executable='joystick_control.py',
        name='joystick_control',
        output='screen',
        emulate_tty=True
    )

    return LaunchDescription([
        joystick_node
    ])