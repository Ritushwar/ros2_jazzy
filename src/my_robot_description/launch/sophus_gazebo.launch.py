import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'sophus_connect.urdf.xacro')
    bridge_config = os.path.join(pkg_share, 'config', 'bridge.yaml')
    share_root = os.path.dirname(pkg_share)

    gz_plugin_dir = '/opt/ros/jazzy/opt/gz_sim_vendor/lib/gz-sim-8/plugins'

    gz_env = dict(os.environ)
    gz_env['GZ_SIM_RESOURCE_PATH'] = share_root + (
        ':' + gz_env['GZ_SIM_RESOURCE_PATH'] if gz_env.get('GZ_SIM_RESOURCE_PATH') else ''
    )
    gz_env['GZ_SIM_SYSTEM_PLUGIN_PATH'] = gz_plugin_dir + (
        ':' + gz_env['GZ_SIM_SYSTEM_PLUGIN_PATH'] if gz_env.get('GZ_SIM_SYSTEM_PLUGIN_PATH') else ''
    )

    robot_description = Command(['xacro ', xacro_file])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    gz_sim = ExecuteProcess(
        cmd=['bash', '-c', 'echo "GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH"; exec gz sim -r empty.sdf'],
        output='screen',
        env=gz_env,
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', 'empty',
            '-topic', 'robot_description',
            '-name', 'sophus',
            '-z', '0.07'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config}],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        gz_sim,
        spawn_entity,
        bridge,
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),
    ])