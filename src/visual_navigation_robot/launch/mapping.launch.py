import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('visual_navigation_robot')

    sensor_config_arg = DeclareLaunchArgument(
        'sensor_config',
        default_value='s4',
        description='Sensor Fusion Configuration Profile (s1, s2, s3, s4)'
    )

    sensor_config = LaunchConfiguration('sensor_config')

    # Visual Odometry Node
    visual_odometry_node = Node(
        package='visual_navigation_robot',
        executable='visual_odometry_node',
        name='visual_odometry_node',
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # Ground Truth Publisher Node
    ground_truth_node = Node(
        package='visual_navigation_robot',
        executable='ground_truth_publisher',
        name='ground_truth_publisher',
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # Robot Localization EKF Node
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[
            os.path.join(pkg_share, 'config', 'ekf_s4_full_fusion.yaml'),
            {'use_sim_time': True}
        ]
    )

    return LaunchDescription([
        sensor_config_arg,
        visual_odometry_node,
        ground_truth_node,
        ekf_node
    ])