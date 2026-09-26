#!/usr/bin/env python3

import os
import math
import yaml

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from visualization_msgs.msg import Marker
from ament_index_python.packages import get_package_share_directory


class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')

        # Declare ROS 2 parameters
        self.declare_parameter('location', '')
        self.declare_parameter('goal_x', 0.0)
        self.declare_parameter('goal_y', 0.0)
        self.declare_parameter('linear_speed', 0.3)
        self.declare_parameter('angular_speed', 0.8)
        self.declare_parameter('tolerance', 0.2)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        self.tolerance = self.get_parameter('tolerance').value

        # Set initial target
        location_name = self.get_parameter('location').value
        self.target_x = self.get_parameter('goal_x').value
        self.target_y = self.get_parameter('goal_y').value

        if location_name:
            self.load_location(location_name)

        # Publishers & Subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.marker_pub = self.create_publisher(Marker, '/goal_marker', 10)
        
        # Subscribe to Web Dashboard Room Commands
        self.room_sub = self.create_subscription(
            String,
            '/selected_room',
            self.room_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.odom_callback,
            10
        )

        self.get_logger().info("Waypoint Navigator Active & Listening for Web UI Dispatch...")

    def load_location(self, location_name):
        try:
            pkg_share = get_package_share_directory('visual_navigation_robot')
            config_path = os.path.join(pkg_share, 'config', 'building_locations.yaml')

            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    data = yaml.safe_load(f)

                if 'locations' in data and location_name in data['locations']:
                    loc_info = data['locations'][location_name]
                    self.target_x = float(loc_info['x'])
                    self.target_y = float(loc_info['y'])
                    self.get_logger().info(
                        f"Web Dispatch received -> Setting target '{location_name}': ({self.target_x}, {self.target_y})"
                    )
                else:
                    self.get_logger().error(f"Location '{location_name}' not found in building_locations.yaml!")
        except Exception as e:
            self.get_logger().error(f"Failed to parse location configuration: {str(e)}")

    def room_callback(self, msg: String):
        location_name = msg.data.strip()
        self.load_location(location_name)

    def publish_goal_marker(self):
        marker = Marker()
        marker.header.frame_id = "odom"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "goal"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = self.target_x
        marker.pose.position.y = self.target_y
        marker.pose.position.z = 0.2
        marker.scale.x = 0.3
        marker.scale.y = 0.3
        marker.scale.z = 0.3
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        self.marker_pub.publish(marker)

    def odom_callback(self, msg: Odometry):
        self.publish_goal_marker()

        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y

        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        siny_cosp = 2.0 * (qw * qz + qx * qy)
        cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
        curr_yaw = math.atan2(siny_cosp, cosy_cosp)

        dx = self.target_x - curr_x
        dy = self.target_y - curr_y
        distance = math.hypot(dx, dy)
        target_yaw = math.atan2(dy, dx)
        heading_error = math.atan2(math.sin(target_yaw - curr_yaw), math.cos(target_yaw - curr_yaw))

        cmd = Twist()

        if distance <= self.tolerance:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.cmd_vel_pub.publish(cmd)
            return

        if abs(heading_error) > 0.4:
            cmd.linear.x = 0.0
            cmd.angular.z = self.angular_speed if heading_error > 0 else -self.angular_speed
        else:
            cmd.linear.x = min(self.linear_speed, distance * 0.5)
            cmd.angular.z = heading_error * 1.5

        self.cmd_vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = WaypointNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()