import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    my_pkg = get_package_share_directory('my_robot_description')
    rviz_config = os.path.join(my_pkg, 'rviz', 'rviz.rviz')
    gazebo_models_path, ignore_last_dir = os.path.split(my_pkg)
    os.environ["GZ_SIM_RESOURCE_PATH"] += os.pathsep + gazebo_models_path

    rviz_launch_arg = DeclareLaunchArgument(
        name='rviz', default_value='true',
        description='Open RViz.'
    )

    world_arg = DeclareLaunchArgument(
        name='world', default_value='empty_world.sdf',
        description='Name of the Gazebo world file to load'
    )

    model_arg = DeclareLaunchArgument(
        name='model', default_value='my_bot.urdf',
        description='Name of the URDF description to load'
    )

    # Define the path to your URDF or Xacro file
    urdf_file_path = PathJoinSubstitution([
        my_pkg,  # Replace with your package name
        "urdf",
        LaunchConfiguration('model')  # Replace with your URDF or Xacro file
    ])

    # Launch Gazebo
    world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(my_pkg, 'launch', 'gazebo.launch.py'),
        ),
        launch_arguments={
        'world': LaunchConfiguration('world'),
        }.items()
    )

    # Launch Rviz optional
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(my_pkg, 'launch', 'rviz_urdf.launch.py'),
        ),
        condition=IfCondition(LaunchConfiguration('rviz')),
        launch_arguments={
        'world': LaunchConfiguration('world'),
        'gui':'true',
        'rvizconfig': rviz_config,
        'model': LaunchConfiguration('model')
        }.items(),
    )

    # Spawn the URDF model using the `/world/<world_name>/create` service
    spawn_urdf_node = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "my_robot",
            "-topic", "robot_description",
            "-x", "0.0", "-y", "0.0", "-z", "0.5", "-Y", "0.0"  # Initial spawn position
        ],
        output="screen",
        parameters=[
            {'use_sim_time': True},
        ]
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': Command(['xacro', ' ', urdf_file_path]),
             'use_sim_time': True},
        ],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    ldo = LaunchDescription()
    ldo.add_action(rviz_launch_arg)
    ldo.add_action(world_arg)
    ldo.add_action(model_arg)
    ldo.add_action(world_launch)
    ldo.add_action(robot_state_publisher_node)
    ldo.add_action(spawn_urdf_node)
    ldo.add_action(rviz_launch)

    return ldo