#!/usr/bin/env python3

import os
import math
import yaml

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from visualization_msgs.msg import Marker
from ament_index_python.packages import get_package_share_directory


class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')

        # Control Parameters
        self.declare_parameter('linear_speed', 0.25)
        self.declare_parameter('angular_speed', 0.6)
        self.declare_parameter('tolerance', 0.18)
        self.declare_parameter('min_wall_distance', 0.45)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        self.tolerance = self.get_parameter('tolerance').value
        self.min_wall_distance = self.get_parameter('min_wall_distance').value

        # Navigation State
        self.waypoints = [(0.0, 0.0)]
        self.current_wp_idx = 0
        self.state = "NAVIGATING"  # NAVIGATING, RECOVERING_BACK, RECOVERING_TURN
        self.recovery_start_time = 0.0
        self.last_progress_time = self.get_clock().now().seconds_nanoseconds()[0]
        self.last_pose = (0.0, 0.0)
        self.obstacle_detected = False

        # Publishers & Subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.marker_pub = self.create_publisher(Marker, '/goal_marker', 10)

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

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.get_logger().info("Collision-Aware Recovery Navigator Active & Ready.")

    def scan_callback(self, msg: LaserScan):
        # Inspect front arc (30 degrees left and right)
        num_ranges = len(msg.ranges)
        if num_ranges == 0:
            return

        front_arc = msg.ranges[:int(num_ranges * 0.083)] + msg.ranges[int(num_ranges * 0.917):]
        valid_ranges = [r for r in front_arc if msg.range_min < r < msg.range_max]

        if valid_ranges and min(valid_ranges) < self.min_wall_distance:
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False

    def room_callback(self, msg: String):
        location_name = msg.data.strip()
        try:
            pkg_share = get_package_share_directory('visual_navigation_robot')
            config_path = os.path.join(pkg_share, 'config', 'building_locations.yaml')

            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    data = yaml.safe_load(f)

                if 'locations' in data and location_name in data['locations']:
                    wp_data = data['locations'][location_name]['waypoints']
                    self.waypoints = [(float(wp['x']), float(wp['y'])) for wp in wp_data]
                    self.current_wp_idx = 0
                    self.state = "NAVIGATING"
                    self.get_logger().info(
                        f"Target Dispatch: '{location_name}' with {len(self.waypoints)} waypoints."
                    )
                else:
                    self.get_logger().error(f"Location '{location_name}' missing in yaml!")
        except Exception as e:
            self.get_logger().error(f"Error loading location dispatch: {str(e)}")

    def publish_goal_marker(self, x, y):
        marker = Marker()
        marker.header.frame_id = "odom"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "goal"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.position.z = 0.2
        marker.scale.x = 0.30
        marker.scale.y = 0.30
        marker.scale.z = 0.30
        marker.color.a = 1.0
        marker.color.g = 1.0
        self.marker_pub.publish(marker)

    def odom_callback(self, msg: Odometry):
        if not self.waypoints or self.current_wp_idx >= len(self.waypoints):
            return

        now = self.get_clock().now().seconds_nanoseconds()[0]
        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y

        # Quaternion to Yaw conversion
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        siny_cosp = 2.0 * (qw * qz + qx * qy)
        cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
        curr_yaw = math.atan2(siny_cosp, cosy_cosp)

        # STUCK DETECTION: Check if robot hasn't moved 0.05m in 4 seconds while navigating
        dist_moved = math.hypot(curr_x - self.last_pose[0], curr_y - self.last_pose[1])
        if dist_moved > 0.05:
            self.last_progress_time = now
            self.last_pose = (curr_x, curr_y)

        is_stuck = (now - self.last_progress_time > 4.0) and (self.state == "NAVIGATING")

        # RECOVERY STATE MACHINE
        if self.state == "RECOVERING_BACK":
            cmd = Twist()
            cmd.linear.x = -0.15  # Back up away from wall
            self.cmd_vel_pub.publish(cmd)

            if now - self.recovery_start_time > 2.0:  # Back up for 2 seconds
                self.state = "RECOVERING_TURN"
                self.recovery_start_time = now
            return

        elif self.state == "RECOVERING_TURN":
            cmd = Twist()
            cmd.angular.z = 0.6  # Rotate to clear orientation
            self.cmd_vel_pub.publish(cmd)

            if now - self.recovery_start_time > 1.5:  # Rotate for 1.5 seconds
                self.state = "NAVIGATING"
                self.last_progress_time = now
            return

        # TRIGGER RECOVERY IF OBSTACLE DETECTED OR STUCK
        if (self.obstacle_detected or is_stuck) and self.state == "NAVIGATING":
            self.get_logger().warn("Obstacle / Stuck detected! Initiating reverse recovery...")
            self.state = "RECOVERING_BACK"
            self.recovery_start_time = now
            return

        # NORMAL NAVIGATION LOGIC
        target_x, target_y = self.waypoints[self.current_wp_idx]
        self.publish_goal_marker(target_x, target_y)

        dx = target_x - curr_x
        dy = target_y - curr_y
        distance = math.hypot(dx, dy)

        if distance <= self.tolerance:
            self.get_logger().info(f"Waypoint {self.current_wp_idx + 1}/{len(self.waypoints)} Reached!")
            self.current_wp_idx += 1
            if self.current_wp_idx >= len(self.waypoints):
                self.cmd_vel_pub.publish(Twist())  # Stop
                self.get_logger().info("Target Destination Reached Successfully!")
            return

        target_yaw = math.atan2(dy, dx)
        heading_error = math.atan2(math.sin(target_yaw - curr_yaw), math.cos(target_yaw - curr_yaw))

        cmd = Twist()
        # Strict turn-in-place: Do NOT move forward if heading error > 0.25 rad (~14 deg)
        if abs(heading_error) > 0.25:
            cmd.linear.x = 0.0
            cmd.angular.z = self.angular_speed if heading_error > 0 else -self.angular_speed
        else:
            cmd.linear.x = min(self.linear_speed, distance * 0.4)
            cmd.angular.z = heading_error * 1.2

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