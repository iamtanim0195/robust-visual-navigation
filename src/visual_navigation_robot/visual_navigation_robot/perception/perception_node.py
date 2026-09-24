import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from visual_navigation_robot.perception.image_preprocessing import ImagePreprocessor
from visual_navigation_robot.perception.feature_extraction import FeatureExtractor
from visual_navigation_robot.perception.feature_tracking import FeatureTracker

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        
        # Subscribes to degraded image stream for experimental evaluation
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_degraded',
            self.image_callback,
            10
        )
        self.publisher_ = self.create_publisher(Image, '/perception/image_features', 10)
        
        self.bridge = CvBridge()
        self.preprocessor = ImagePreprocessor()
        self.extractor = FeatureExtractor(max_corners=200)
        self.tracker = FeatureTracker()

        self.prev_gray = None
        self.prev_pts = None

        self.get_logger().info('Perception Node subscribed to /camera/image_degraded.')

    def image_callback(self, msg: Image):
        try:
            frame_bgr = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'CvBridge exception: {e}')
            return

        curr_gray = self.preprocessor.process(frame_bgr)
        vis_frame = frame_bgr.copy()

        if self.prev_gray is not None and self.prev_pts is not None and len(self.prev_pts) > 10:
            good_new, good_old = self.tracker.track(self.prev_gray, curr_gray, self.prev_pts)

            if good_new is not None:
                for new, old in zip(good_new, good_old):
                    a, b = new.ravel().astype(int)
                    c, d = old.ravel().astype(int)
                    cv2.line(vis_frame, (a, b), (c, d), (0, 255, 0), 2)
                    cv2.circle(vis_frame, (a, b), 4, (0, 0, 255), -1)

                self.prev_pts = good_new.reshape(-1, 1, 2)
            else:
                self.prev_pts = self.extractor.extract_corners(curr_gray)
        else:
            self.prev_pts = self.extractor.extract_corners(curr_gray)

        self.prev_gray = curr_gray.copy()

        out_msg = self.bridge.cv2_to_imgmsg(vis_frame, encoding='bgr8')
        out_msg.header = msg.header
        self.publisher_.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()