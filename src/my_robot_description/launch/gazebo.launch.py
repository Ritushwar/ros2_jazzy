import os
from ament_index_python.packages import get_package_share_directory  # Returns the actual package share directory as a string immediately.
from launch import LaunchDescription  # Creates the main launch description
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription  # Declare launch arguments, Includes another launch file.
from launch.launch_description_sources import PythonLaunchDescriptionSource  #	Loads another Python launch file.
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution  # Retrieves launch argument values

def generate_launch_description():
    world_args = DeclareLaunchArgument(
        name='world', default_value='empty_world.sdf',
        description='Name of the Gazebo world file to load'
    )

    my_pkg = get_package_share_directory('my_robot_description')
    my_pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Add your own gazebo 3d models library path here
    gazebo_models_path = "/home/ritu/jazzy_ws/src/my_robot_description/gazebo_models"
    # Adds your custom Gazebo models directory to the environment variable so Gazebo can find and load your models
    os.environ["GZ_SIM_RESOURCE_PATH"] += os.pathsep + gazebo_models_path
    
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(my_pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args' :[PathJoinSubstitution([
            my_pkg,
            'worlds',
            LaunchConfiguration('world')
        ]),
            TextSubstitution(text=' -r -v1')],
            'on_exit_shutdown': 'true'}.items()
    )
    ldo = LaunchDescription()
    ldo.add_action(world_args)
    ldo.add_action(gazebo_launch)

    return ldo