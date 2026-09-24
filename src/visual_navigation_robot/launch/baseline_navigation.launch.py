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
    goal_x = LaunchConfiguration('goal_x', default='2.0')
    goal_y = LaunchConfiguration('goal_y', default='0.0')

    mapping_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'mapping.launch.py')
        ),
        launch_arguments={'sensor_config': sensor_config}.items()
    )

    node_navigator = Node(
        package='visual_navigation_robot',
        executable='waypoint_navigator',
        name='waypoint_navigator',
        output='screen',
        parameters=[{
            'goal_x': goal_x,
            'goal_y': goal_y,
            'use_sim_time': True
        }]
    )

    node_logger = Node(
        package='visual_navigation_robot',
        executable='experiment_logger',
        name='experiment_logger',
        output='screen',
        parameters=[{
            'sensor_config': sensor_config,
            'degradation_type': 'clean',
            'use_sim_time': True
        }]
    )

    return LaunchDescription([
        DeclareLaunchArgument('sensor_config', default_value='s4'),
        DeclareLaunchArgument('goal_x', default_value='2.0'),
        DeclareLaunchArgument('goal_y', default_value='0.0'),
        mapping_launch,
        node_navigator,
        node_logger
    ])