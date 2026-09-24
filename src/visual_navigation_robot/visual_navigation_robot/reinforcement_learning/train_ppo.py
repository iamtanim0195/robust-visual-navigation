import os
import rclpy
from visual_navigation_robot.reinforcement_learning.nav_gym_env import RobotNavEnv

try:
    from stable_baselines3 import PPO
    HAS_SB3 = True
except ImportError:
    HAS_SB3 = False

def main():
    rclpy.init()
    node = rclpy.create_node('ppo_training_node')

    env = RobotNavEnv(node=node, goal_x=2.0, goal_y=0.0)

    if not HAS_SB3:
        node.get_logger().error("Stable-Baselines3 not installed. Install via 'pip install stable-baselines3' to run PPO training.")
        rclpy.shutdown()
        return

    out_dir = 'experiments/models'
    os.makedirs(out_dir, exist_ok=True)

    node.get_logger().info("Initializing PPO Training Agent...")
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003, n_steps=2048)

    model.learn(total_timesteps=10000)
    model_path = os.path.join(out_dir, "ppo_navigation_model.zip")
    model.save(model_path)
    node.get_logger().info(f"PPO Policy model saved successfully to {model_path}")

    rclpy.shutdown()

if __name__ == '__main__':
    main()