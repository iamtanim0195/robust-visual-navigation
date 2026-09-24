import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class VisualDegradationNode(Node):
    def __init__(self):
        super().__init__('visual_degradation_node')

        self.declare_parameter('degradation_mode', 'clean')  # clean, blur, resolution, illumination
        self.declare_parameter('severity_level', 0)          # 0, 1, 2, 3

        self.deg_mode = self.get_parameter('degradation_mode').value
        self.severity = self.get_parameter('severity_level').value

        self.sub_raw = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.pub_deg = self.create_publisher(Image, '/camera/image_degraded', 10)

        self.bridge = CvBridge()
        self.get_logger().info(f'Visual Degradation Node Active. Mode: {self.deg_mode} | Level: {self.severity}')

    def apply_degradation(self, img: np.ndarray) -> np.ndarray:
        if self.severity == 0 or self.deg_mode == 'clean':
            return img

        h, w = img.shape[:2]

        if self.deg_mode == 'blur':
            # Kernel sizes: Level 1 (k=7), Level 2 (k=15), Level 3 (k=27)
            ksize = [1, 7, 15, 27][min(self.severity, 3)]
            return cv2.GaussianBlur(img, (ksize, ksize), 0)

        elif self.deg_mode == 'resolution':
            # Scale factors: Level 1 (0.5), Level 2 (0.25), Level 3 (0.125)
            scale = [1.0, 0.5, 0.25, 0.125][min(self.severity, 3)]
            small = cv2.resize(img, (max(1, int(w * scale)), max(1, int(h * scale))), interpolation=cv2.INTER_LINEAR)
            return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

        elif self.deg_mode == 'illumination':
            # Factor: Level 1 (0.5), Level 2 (0.2), Level 3 (0.05)
            factor = [1.0, 0.5, 0.2, 0.05][min(self.severity, 3)]
            return np.clip(img.astype(np.float32) * factor, 0, 255).astype(np.uint8)

        return img

    def image_callback(self, msg: Image):
        try:
            frame_bgr = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'CvBridge exception: {e}')
            return

        degraded_frame = self.apply_degradation(frame_bgr)

        out_msg = self.bridge.cv2_to_imgmsg(degraded_frame, encoding='bgr8')
        out_msg.header = msg.header
        self.pub_deg.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = VisualDegradationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()