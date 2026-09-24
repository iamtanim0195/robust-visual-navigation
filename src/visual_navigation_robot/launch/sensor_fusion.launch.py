import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def launch_setup(context, *args, **kwargs):
    pkg_share = get_package_share_directory('visual_navigation_robot')
    config_name = LaunchConfiguration('sensor_config').perform(context).lower()

    config_map = {
        's1': 'ekf_s1_vision_only.yaml',
        's2': 'ekf_s2_vision_wheel.yaml',
        's3': 'ekf_s3_vision_imu.yaml',
        's4': 'ekf_s4_full_fusion.yaml'
    }

    if config_name not in config_map:
        raise ValueError(f"Invalid sensor_config '{config_name}'. Choose from: s1, s2, s3, s4.")

    ekf_config_file = os.path.join(pkg_share, 'config', config_map[config_name])

    node_ekf = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_file, {'use_sim_time': True}],
        remappings=[('/odometry/filtered', '/odometry/filtered')]
    )

    return [node_ekf]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'sensor_config',
            default_value='s4',
            description='Sensor configuration mode: s1 (Vision Only), s2 (Vision+Wheel), s3 (Vision+IMU), s4 (Full Fusion)'
        ),
        OpaqueFunction(function=launch_setup)
    ])