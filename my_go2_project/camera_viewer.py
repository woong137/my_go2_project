import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraViewer(Node):

    def __init__(self):
        super().__init__('camera_viewer')
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.listener_callback, 10)
        self.subscription
        self.br = CvBridge()
        self.get_logger().info('CameraViewer node started.')

    def listener_callback(self, data):
        try:
            # ROS Image → OpenCV 이미지로 변환
            current_frame = self.br.imgmsg_to_cv2(data, "bgr8")

            # 화면에 영상 표시
            cv2.imshow("Camera View", current_frame)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f'Error converting image: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = CameraViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
