import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'visual_navigation_robot'
    pkg_share = get_package_share_directory(pkg_name)
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    # Paths
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')
    world_file = os.path.join(pkg_share, 'worlds', 'research_world.sdf')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'robot_view.rviz')

    # Robot Description
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # ROS Nodes
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    # Gazebo Sim Launch
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    # Spawn Robot Entity
    node_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'visual_navigation_robot',
            '-z', '0.1'
        ],
        output='screen'
    )

    # ROS-Gazebo Topic Bridge
    node_ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            # Camera Bridges
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            # IMU Bridge
            '/imu/data@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/world/research_world/model/visual_navigation_robot/link/imu_link/sensor/imu_sensor/imu@sensor_msgs/msg/Imu[gz.msgs.IMU'
        ],
        remappings=[
            ('/world/research_world/model/visual_navigation_robot/link/imu_link/sensor/imu_sensor/imu', '/imu/data')
        ],
        output='screen'
    )

    # RViz2 Node
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo_sim,
        node_spawn_entity,
        node_ros_gz_bridge,
        node_rviz
    ])