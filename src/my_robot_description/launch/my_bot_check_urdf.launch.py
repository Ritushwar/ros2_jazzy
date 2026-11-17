import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    my_robot_description = FindPackageShare('my_robot_description')
    default_rviz_configuration_path = PathJoinSubstitution([my_robot_description, 'rviz', 'urdf.rviz'])

    # show joint state publisher GUI for joints
    gui_args = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
                                     description='Flag to enable joint_state_publisher_gui')
    
    # add Rviz Config file
    rviz_args = DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_configuration_path,
                                      description="Absolute path to rviz config file")
    
    # urdf model path within the my_robot_description
    model_args = DeclareLaunchArgument(
        'model', default_value='my_bot.urdf',
        description='URDF description to load'
    )

    # Use built-in ROS2 URDF launch package with our own arguments
    urdf = IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('urdf_launch'), 'launch', 'display.launch.py']),
        launch_arguments={
            'urdf_package':'my_robot_description',
            'urdf_package_path': PathJoinSubstitution(['urdf',LaunchConfiguration('model')]),
            'rviz_config': LaunchConfiguration('rvizconfig'),
            'jsp_gui': LaunchConfiguration('gui')}.items()
    )
    ldo = LaunchDescription()
    ldo.add_action(gui_args)
    ldo.add_action(rviz_args)
    ldo.add_action(model_args)
    ldo.add_action(urdf)
    return ldo

    

