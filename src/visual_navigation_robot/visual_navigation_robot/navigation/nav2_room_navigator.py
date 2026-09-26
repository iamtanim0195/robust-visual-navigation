#!/usr/bin/env python3

import os
import yaml
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from ament_index_python.packages import get_package_share_directory


class Nav2RoomNavigator(Node):
    def __init__(self):
        super().__init__('nav2_room_navigator')

        self.navigator = BasicNavigator()

        # Subscribe to Web UI Dispatch topic
        self.room_sub = self.create_subscription(
            String,
            '/selected_room',
            self.room_callback,
            10
        )

        self.get_logger().info("Nav2 Room Navigator Active & Ready for Web Dispatch...")

    def room_callback(self, msg: String):
        location_name = msg.data.strip()
        self.get_logger().info(f"Received Web Dispatch command: '{location_name}'")

        try:
            pkg_share = get_package_share_directory('visual_navigation_robot')
            config_path = os.path.join(pkg_share, 'config', 'building_locations.yaml')

            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    data = yaml.safe_load(f)

                if 'locations' in data and location_name in data['locations']:
                    loc_info = data['locations'][location_name]
                    target_x = float(loc_info['x'])
                    target_y = float(loc_info['y'])
                    target_yaw = float(loc_info.get('yaw', 0.0))

                    self.send_nav2_goal(target_x, target_y, target_yaw, location_name)
                else:
                    self.get_logger().error(f"Location '{location_name}' not found in building_locations.yaml")
            else:
                self.get_logger().error(f"Config file not found at: {config_path}")
        except Exception as e:
            self.get_logger().error(f"Error processing navigation goal: {str(e)}")

    def send_nav2_goal(self, x, y, yaw, location_name):
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = 0.0

        # Simple Yaw Quaternion conversion around Z-axis
        import math
        goal_pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal_pose.pose.orientation.w = math.cos(yaw / 2.0)

        self.get_logger().info(f"Nav2: Planning global path to {location_name} ({x:.2f}, {y:.2f})...")
        self.navigator.goToPose(goal_pose)


def main(args=None):
    rclpy.init(args=args)
    node = Nav2RoomNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()