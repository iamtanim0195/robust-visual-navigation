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
    deg_mode = LaunchConfiguration('degradation_mode', default='blur')
    severity = LaunchConfiguration('severity_level', default='2')

    baseline_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'baseline_navigation.launch.py')
        ),
        launch_arguments={'sensor_config': sensor_config}.items()
    )

    node_degradation = Node(
        package='visual_navigation_robot',
        executable='visual_degradation_node',
        name='visual_degradation_node',
        output='screen',
        parameters=[{
            'degradation_mode': deg_mode,
            'severity_level': severity,
            'use_sim_time': True
        }]
    )

    return LaunchDescription([
        DeclareLaunchArgument('sensor_config', default_value='s4'),
        DeclareLaunchArgument('degradation_mode', default_value='blur'),
        DeclareLaunchArgument('severity_level', default_value='2'),
        baseline_launch,
        node_degradation
    ])