import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import time
from std_srvs.srv import Empty


class PersonGreeter(Node):
    def __init__(self):
        super().__init__('person_greeter')
        self.bridge = CvBridge()
        self.model = YOLO('yolov8n.pt')

        # Service Client setup
        self.cli = self.create_client(Empty, '/wave')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /wave service to be available...')

        self.sub = self.create_subscription(
            Image, '/image_raw', self.callback, 10)

        # Cooldown variables
        self.last_call_time = 0
        self.cooldown_duration = 10.0  # seconds

        self.get_logger().info("person_greeter node Started")

    def call_wave_service(self):
        current_time = time.time()
        # Only call if the cooldown period has passed
        if (current_time - self.last_call_time) > self.cooldown_duration:
            req = Empty.Request()
            self.cli.call_async(req)
            self.get_logger().info("Human detected! Calling /wave service.")
            self.last_call_time = current_time
        else:
            self.get_logger().debug("Human detected, but service is on cooldown.")

    def callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # Predict humans only (class 0)
        results = self.model.predict(frame, classes=[0], verbose=False)

        # If at least one human is detected
        if len(results[0].boxes) > 0:
            self.call_wave_service()

        annotated = results[0].plot()
        cv2.imshow("Human Detection", annotated)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = PersonGreeter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node...")
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
