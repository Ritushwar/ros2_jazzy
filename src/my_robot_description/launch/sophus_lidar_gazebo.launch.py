import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

# ---- World selection ----
WORLD_FILE = 'cafe_world.sdf'    # CHANGED: was 'empty_world.sdf'
WORLD_NAME = 'cafe'              # CHANGED: must match <world name="..."> in the SDF

def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'sophus_lidar_connect.urdf.xacro')
    bridge_config = os.path.join(pkg_share, 'config', 'bridge.yaml')
    share_root = os.path.dirname(pkg_share)
    models_dir = os.path.join(pkg_share, 'model')   # CHANGED: local models folder not required if fetched through the url

    gz_plugin_dir = '/opt/ros/jazzy/opt/gz_sim_vendor/lib/gz-sim-8/plugins'

    gz_env = dict(os.environ)

    # Uncomment for empty world
    # gz_env['GZ_SIM_RESOURCE_PATH'] = share_root + (
    #     ':' + gz_env['GZ_SIM_RESOURCE_PATH'] if gz_env.get('GZ_SIM_RESOURCE_PATH') else ''
    # )

    # comment out for empty world
    gz_env['GZ_SIM_RESOURCE_PATH'] = models_dir + ':' + share_root + (
        ':' + gz_env['GZ_SIM_RESOURCE_PATH'] if gz_env.get('GZ_SIM_RESOURCE_PATH') else ''
    )
    
    gz_env['GZ_SIM_SYSTEM_PLUGIN_PATH'] = gz_plugin_dir + (
        ':' + gz_env['GZ_SIM_SYSTEM_PLUGIN_PATH'] if gz_env.get('GZ_SIM_SYSTEM_PLUGIN_PATH') else ''
    )

    robot_description = Command(['xacro ', xacro_file])
    robot_description_param = ParameterValue(robot_description, value_type=str)

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_param,
                     'use_sim_time': True}],
        output='screen'
    )

    world_file = os.path.join(pkg_share, 'worlds', WORLD_FILE)

    gz_sim = ExecuteProcess(
        cmd=['bash', '-c', f'exec gz sim -r {world_file}'],
        output='screen',
        env=gz_env,
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', WORLD_NAME,        # CHANGED: was 'empty'
            '-topic', 'robot_description',
            '-name', 'sophus',
            '-x', '0.0', '-y', '0.0',    # CHANGED: explicit spawn pose, adjust if you land inside furniture
            '-z', '0.05'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config,
                     'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        gz_sim,
        spawn_entity,
        bridge,
    ])