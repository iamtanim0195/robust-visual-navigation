import math
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from cv_bridge import CvBridge

from visual_navigation_robot.perception.image_preprocessing import ImagePreprocessor
from visual_navigation_robot.perception.feature_extraction import FeatureExtractor
from visual_navigation_robot.perception.feature_tracking import FeatureTracker

def yaw_to_quaternion(yaw: float) -> Quaternion:
    q = Quaternion()
    q.x = 0.0
    q.y = 0.0
    q.z = math.sin(yaw / 2.0)
    q.w = math.cos(yaw / 2.0)
    return q

class VisualOdometryNode(Node):
    def __init__(self):
        super().__init__('visual_odometry_node')

        # Subscribes to degraded image stream
        self.sub_image = self.create_subscription(Image, '/camera/image_degraded', self.image_callback, 10)
        self.sub_info = self.create_subscription(CameraInfo, '/camera/camera_info', self.info_callback, 10)
        self.pub_vo = self.create_publisher(Odometry, '/visual_odometry/odom', 10)

        self.bridge = CvBridge()
        self.preprocessor = ImagePreprocessor()
        self.extractor = FeatureExtractor(max_corners=300)
        self.tracker = FeatureTracker()

        self.K = np.array([
            [500.0, 0.0, 320.0],
            [0.0, 500.0, 240.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float64)

        self.prev_gray = None
        self.prev_pts = None

        self.cur_x = 0.0
        self.cur_y = 0.0
        self.cur_yaw = 0.0

        self.get_logger().info('Visual Odometry Node subscribed to /camera/image_degraded.')

    def info_callback(self, msg: CameraInfo):
        if msg.k[0] != 0:
            self.K = np.array(msg.k, dtype=np.float64).reshape((3, 3))

    def image_callback(self, msg: Image):
        try:
            frame_bgr = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'CvBridge exception: {e}')
            return

        curr_gray = self.preprocessor.process(frame_bgr)

        if self.prev_gray is not None and self.prev_pts is not None and len(self.prev_pts) >= 8:
            good_new, good_old = self.tracker.track(self.prev_gray, curr_gray, self.prev_pts)

            if good_new is not None and len(good_new) >= 8:
                E, mask = cv2.findEssentialMat(
                    good_new, good_old, self.K, method=cv2.RANSAC, prob=0.999, threshold=1.0
                )

                if E is not None and E.shape == (3, 3):
                    _, R, t, mask_pose = cv2.recoverPose(E, good_new, good_old, self.K)

                    d_yaw = math.atan2(R[1, 0], R[0, 0])
                    step_scale = 0.01

                    dx = t[2, 0] * step_scale
                    dy = -t[0, 0] * step_scale

                    self.cur_yaw += d_yaw
                    self.cur_x += dx * math.cos(self.cur_yaw) - dy * math.sin(self.cur_yaw)
                    self.cur_y += dx * math.sin(self.cur_yaw) + dy * math.cos(self.cur_yaw)

                    self.publish_vo_odometry(msg.header)

                self.prev_pts = good_new.reshape(-1, 1, 2)
            else:
                self.prev_pts = self.extractor.extract_corners(curr_gray)
        else:
            self.prev_pts = self.extractor.extract_corners(curr_gray)

        self.prev_gray = curr_gray.copy()

    def publish_vo_odometry(self, header):
        vo_msg = Odometry()
        vo_msg.header = header
        vo_msg.header.frame_id = 'odom'
        vo_msg.child_frame_id = 'base_footprint'

        vo_msg.pose.pose.position.x = float(self.cur_x)
        vo_msg.pose.pose.position.y = float(self.cur_y)
        vo_msg.pose.pose.position.z = 0.0
        vo_msg.pose.pose.orientation = yaw_to_quaternion(self.cur_yaw)

        self.pub_vo.publish(vo_msg)

def main(args=None):
    rclpy.init(args=args)
    node = VisualOdometryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()