import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('visual_navigation_robot')
    sensor_config = LaunchConfiguration('sensor_config', default='s4')

    vo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'visual_odometry.launch.py')
        )
    )

    ekf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'sensor_fusion.launch.py')
        ),
        launch_arguments={'sensor_config': sensor_config}.items()
    )

    node_ground_truth = Node(
        package='visual_navigation_robot',
        executable='ground_truth_publisher',
        name='ground_truth_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'sensor_config',
            default_value='s4',
            description='Sensor configuration: s1, s2, s3, s4'
        ),
        vo_launch,
        ekf_launch,
        node_ground_truth
    ])