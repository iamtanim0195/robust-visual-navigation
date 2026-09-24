import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage

class GroundTruthPublisher(Node):
    def __init__(self):
        super().__init__('ground_truth_publisher')

        self.subscription = self.create_subscription(
            TFMessage,
            '/tf',
            self.tf_callback,
            10
        )
        self.publisher_ = self.create_publisher(Odometry, '/ground_truth/odom', 10)
        self.get_logger().info('Ground Truth Publisher Node active.')

    def tf_callback(self, msg: TFMessage):
        for transform in msg.transforms:
            # Match Gazebo simulation world transform to robot footprint
            if transform.header.frame_id in ['research_world', 'world', 'odom'] and transform.child_frame_id == 'base_footprint':
                gt_msg = Odometry()
                gt_msg.header = transform.header
                gt_msg.header.frame_id = 'world'
                gt_msg.child_frame_id = 'base_footprint'

                gt_msg.pose.pose.position.x = transform.transform.translation.x
                gt_msg.pose.pose.position.y = transform.transform.translation.y
                gt_msg.pose.pose.position.z = transform.transform.translation.z
                gt_msg.pose.pose.orientation = transform.transform.rotation

                self.publisher_.publish(gt_msg)

def main(args=None):
    rclpy.init(args=args)
    node = GroundTruthPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()