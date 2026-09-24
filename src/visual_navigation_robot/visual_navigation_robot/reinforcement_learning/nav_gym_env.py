import math
import time
import numpy as np
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:
    import gym
    from gym import spaces

class RobotNavEnv(gym.Env):
    def __init__(self, node: Node, goal_x=2.0, goal_y=0.0):
        super(RobotNavEnv, self).__init__()

        self.node = node
        self.goal_x = goal_x
        self.goal_y = goal_y

        # Action Space: [linear_velocity (0 to 0.4 m/s), angular_velocity (-1.0 to 1.0 rad/s)]
        self.action_space = spaces.Box(
            low=np.array([0.0, -1.0], dtype=np.float32),
            high=np.array([0.4, 1.0], dtype=np.float32)
        )

        # Observation Space: [distance_to_goal, heading_error, current_v_x, current_w_z]
        self.observation_space = spaces.Box(
            low=np.array([0.0, -np.pi, -0.5, -2.0], dtype=np.float32),
            high=np.array([10.0, np.pi, 0.5, 2.0], dtype=np.float32)
        )

        self.pub_cmd = self.node.create_publisher(Twist, '/cmd_vel', 10)
        self.sub_odom = self.node.create_subscription(Odometry, '/odometry/filtered', self._odom_cb, 10)

        self.current_odom = None
        self.prev_dist = None

    def _odom_cb(self, msg: Odometry):
        self.current_odom = msg

    def _get_obs(self):
        if self.current_odom is None:
            return np.zeros(4, dtype=np.float32)

        p = self.current_odom.pose.pose.position
        q = self.current_odom.pose.pose.orientation
        v = self.current_odom.twist.twist.linear.x
        w = self.current_odom.twist.twist.angular.z

        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        dx = self.goal_x - p.x
        dy = self.goal_y - p.y
        dist = math.hypot(dx, dy)

        target_yaw = math.atan2(dy, dx)
        heading_err = math.atan2(math.sin(target_yaw - yaw), math.cos(target_yaw - yaw))

        return np.array([dist, heading_err, v, w], dtype=np.float32)

    def step(self, action):
        rclpy.spin_once(self.node, timeout_sec=0.05)

        cmd = Twist()
        cmd.linear.x = float(action[0])
        cmd.angular.z = float(action[1])
        self.pub_cmd.publish(cmd)

        time.sleep(0.05)
        rclpy.spin_once(self.node, timeout_sec=0.05)

        obs = self._get_obs()
        dist, heading_err = obs[0], obs[1]

        # Reward formulation: distance progress + heading alignment penalty
        reward = 0.0
        if self.prev_dist is not None:
            reward += (self.prev_dist - dist) * 10.0

        reward -= abs(heading_err) * 0.1
        self.prev_dist = dist

        done = False
        if dist < 0.2:
            reward += 100.0
            done = True

        return obs, reward, done, False, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.prev_dist = None
        obs = self._get_obs()
        return obs, {}