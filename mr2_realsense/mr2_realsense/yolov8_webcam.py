import os
import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Int32, String

from ultralytics import YOLO

class YOLODetector(Node):
    
    def __init__(self):
        super().__init__('yolo_detector')
        self.model = YOLO(os.path.join(os.environ['HOME'], '/home/vipho/ai/yolov9_rs', 'yolov9_3color.pt'))
        self.bridge = CvBridge()
        self.image_publisher = self.create_publisher(Image, 'webcam_image', 10)  
        self.ball_count_publisher = self.create_publisher(Int32, '/total_ball_count', 10)
        self.ball_class_publisher = self.create_publisher(String, '/ball_class', 10) 

        self.timer = self.create_timer(0.1, self.detect_objects)
        self.W = 640
        self.H = 480
        self.capture = cv2.VideoCapture(0) 

    def detect_objects(self):
       
        self.red_ball_counter = 0
        self.blue_ball_counter = 0
        
        ret, color_image = self.capture.read() 
        if not ret:
            return

        results = self.model(color_image)

        for r in results:
            boxes = r.boxes
            for box in boxes:
               
                c = box.cls  
                class_name = self.model.names[int(c)] 
    
                if int(c) == 1:
                    ball_class = "blue ball" if class_name == "blue" else "red ball"
                    self.red_ball_counter += 1
                elif int(c) == 0:
                    self.blue_ball_counter += 1
                    pass

        total_count = self.red_ball_counter + self.blue_ball_counter
        total_count_msg = Int32()
        total_count_msg.data = total_count
        
        self.get_logger().info(f'Red balls: {self.red_ball_counter}, Blue balls: {self.blue_ball_counter}, Total balls: {total_count}')
        self.ball_count_publisher.publish(total_count_msg)
        
        self.ball_class_publisher.publish(String(data=ball_class))

        annotated_frame = results[0].plot()

        ros_image = self.bridge.cv2_to_imgmsg(annotated_frame, "bgr8")
        self.image_publisher.publish(ros_image)


def main(args=None):
    rclpy.init(args=args)
    yolo_detector = YOLODetector()
    try:
        rclpy.spin(yolo_detector)
    except KeyboardInterrupt:
        pass
    yolo_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
