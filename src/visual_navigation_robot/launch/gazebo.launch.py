import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('visual_navigation_robot')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    default_world_path = os.path.join(pkg_share, 'worlds', 'building_world.sdf')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world_path,
        description='Path to SDF world file'
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': PathJoinSubstitution(['-r -v 4 ', LaunchConfiguration('world')])
        }.items()
    )

    urdf_path = os.path.join(pkg_share, 'urdf', 'robot.urdf')
    with open(urdf_path, 'r') as infp:
        robot_description_raw = infp.read()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': True
        }]
    )

    node_ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/model/visual_navigation_robot/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/imu/data@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/goal_marker@visualization_msgs/msg/Marker[gz.msgs.Marker'
        ],
        output='screen'
    )
    
    return LaunchDescription([
        world_arg,
        gz_sim,
        robot_state_publisher_node,
        node_ros_gz_bridge
    ])