import os
import csv
import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class ExperimentLogger(Node):
    def __init__(self):
        super().__init__('experiment_logger')

        self.declare_parameter('sensor_config', 's4')
        self.declare_parameter('degradation_type', 'clean')
        self.declare_parameter('output_dir', 'experiments/raw')

        self.config_name = self.get_parameter('sensor_config').value
        self.deg_type = self.get_parameter('degradation_type').value
        self.out_dir = self.get_parameter('output_dir').value

        # Make sure directory exists on initialization
        os.makedirs(self.out_dir, exist_ok=True)
        self.log_file = os.path.join(self.out_dir, f'trial_{self.config_name}_{self.deg_type}.csv')

        self.sub_est = self.create_subscription(Odometry, '/odometry/filtered', self.est_callback, 10)
        self.sub_gt = self.create_subscription(Odometry, '/ground_truth/odom', self.gt_callback, 10)

        self.latest_gt = None
        self.squared_errors = []
        self.path_length = 0.0
        self.prev_x = None
        self.prev_y = None

        self.csv_handle = open(self.log_file, 'w', newline='')
        self.writer = csv.writer(self.csv_handle)
        self.writer.writerow(['timestamp_sec', 'gt_x', 'gt_y', 'est_x', 'est_y', 'error_m'])
        self.csv_handle.flush()

        self.get_logger().info(f'Experiment Logger active. Writing to: {self.log_file}')

    def gt_callback(self, msg: Odometry):
        self.latest_gt = msg.pose.pose.position

    def est_callback(self, msg: Odometry):
        if self.latest_gt is None:
            return

        est_p = msg.pose.pose.position
        gt_p = self.latest_gt

        err = math.hypot(est_p.x - gt_p.x, est_p.y - gt_p.y)
        self.squared_errors.append(err ** 2)

        sec = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        self.writer.writerow([sec, gt_p.x, gt_p.y, est_p.x, est_p.y, err])
        self.csv_handle.flush()

        if self.prev_x is not None:
            self.path_length += math.hypot(gt_p.x - self.prev_x, gt_p.y - self.prev_y)

        self.prev_x = gt_p.x
        self.prev_y = gt_p.y

    def compute_ate(self) -> float:
        if not self.squared_errors:
            return 0.0
        return math.sqrt(sum(self.squared_errors) / len(self.squared_errors))

    def destroy_node(self):
        ate = self.compute_ate()
        self.get_logger().info(f'FINAL TRIAL SUMMARY: ATE={ate:.4f} m | Path Length={self.path_length:.2f} m')
        if not self.csv_handle.closed:
            self.csv_handle.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ExperimentLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()