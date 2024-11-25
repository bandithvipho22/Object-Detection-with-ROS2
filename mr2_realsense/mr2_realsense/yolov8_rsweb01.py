import os
import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String, Int32, UInt16, Int8MultiArray
import pyrealsense2 as rs
from ultralytics import YOLO

class YOLODetector(Node):
    
    def __init__(self):
        super().__init__('yolo_detector')
        # self.model = YOLO(os.path.join(os.environ['HOME'], 'yolov8_rs', 'ball_yolov8t03.engine')) 
        self.model = YOLO(os.path.join(os.environ['HOME'], 'yolov8_rs', 'ball_yolov8t05.engine')) 
        self.ball_distance_publisher = self.create_publisher(Float32MultiArray, '/ball_distance', 10)
        self.ball_count_publisher = self.create_publisher(Int8MultiArray, '/total_ball_count', 10)
        self.ball_class_publisher = self.create_publisher(String, '/ball_class', 10) 
        self.ball_silo_publisher = self.create_publisher(String, '/ball_silo', 10)
        self.laser_sub = self.create_subscription(Float32MultiArray, '/laser', self.laser_callback, 10)
        self.state_sub = self.create_subscription(UInt16 , '/state', self.state_callback , 10)
        self.timer = self.create_timer(0.1, self.detect_objects)
        self.W = 640
        self.H = 480
        self.HFOV = 62
        
        # self.fx = 617.344 #607.5303
        # self.fy = 617.344 #607.0724
        self.ball_silo = None
        self.total_count = 0
        self.laserX = 0.0
        self.laserY = 0.0
        self.state = 0
        self.cammera = None
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.W, self.H, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.depth, self.W, self.H, rs.format.z16, 30)
        self.profile = self.pipeline.start(self.config)
        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)
        self.capture = cv2.VideoCapture(2) 
        self.logger = self.get_logger()
    
    def laser_callback(self, laser):
        self.laserX = laser.data[0]
        self.laserY = laser.data[1]
    
    def state_callback(self, state):
        self.state = state.data
        
    def detect_objects(self):
        if (self.state == 10):
            self.red_ball_counter = 0
            self.blue_ball_counter = 0
            ret, color_image = self.capture.read() 
            self.cammera = "webcame"
            if not ret:
                return
            results = self.model(color_image)
        else: 
            ball_class = "no_ball"
            self.min_distance = float('inf')  # Reset min_distance for each detection cycle
            self.nearest_object = None  # Reset nearest_object for each detection cycle
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()
            if not color_frame:
                return
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            self.cammera = "realsense"
            results = self.model(color_image)
        self.get_logger().info("%s is OPEN"%self.cammera)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0].to('cpu').detach().numpy().copy()
                c = box.cls  # Class ID
                class_name = self.model.names[int(c)] 
                
                if (self.cammera == "realsense"):
                    xmin, ymin, xmax, ymax = map(int, b[:4])  
                    x_center = int((xmin + xmax) / 2)
                    y_center = int((ymin + ymax) / 2)
                    # depth = depth_frame.get_distance(x_center, y_center)
                    Horizontal_Angle  = ((x_center - self.W / 2) / (self.W / 2)) * (self.HFOV / 2)

                if int(c) == 1:
                    
                    if (self.cammera == "webcame"):
                        self.red_ball_counter += 1
                    #################################################    
                    elif (self.cammera == "realsense"):   
                        # ball_class = "blue ball" if class_name == 0 else 1
                        ball_class = "blue ball" if class_name == "blue" else "red ball"       
                        object_depth = depth_image[ymin:ymax, xmin:xmax]

                        # Get the median distance within the bounding box
                        median_distance = np.median(object_depth)

                        # Compare to find the nearest object
                        if median_distance < self.min_distance:
                            self.min_distance = median_distance / 1000
                            self.nearest_object = [xmin, ymin, xmax, ymax]
                            self.x_center = x_center
                            self.Horizontal_Angle = Horizontal_Angle
                            # self.min_angle = min_angle
                elif int(c) == 0:
                    if (self.cammera == "webcame"): 
                        self.blue_ball_counter += 1
                    pass
                if (self.cammera == "realsense"): 
                    cv2.rectangle(color_image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                    cv2.putText(color_image, class_name, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        if (self.cammera == "webcame"): 
            self.total_count = self.red_ball_counter + self.blue_ball_counter
            total_count_msg = Int8MultiArray()
            total_count_msg.data = [self.red_ball_counter,self.blue_ball_counter,self.total_count]
            self.get_logger().info(f'Red balls: {self.red_ball_counter}, Blue balls: {self.blue_ball_counter}, Total balls: {self.total_count}')
            self.ball_count_publisher.publish(total_count_msg)
        elif (self.cammera == "realsense"): 
            self.ball_class_publisher.publish(String(data=ball_class))
            if self.nearest_object is not None:
                object_distance = Float32MultiArray()
                object_distance.data = [self.min_distance, self.Horizontal_Angle]
                Yaw = (-1 * (np.pi * self.Horizontal_Angle) / 180 ) + 0.03
                self.ball_distance_publisher.publish(object_distance)
                self.logger.info('distance: %f, radian: %f, degree: %f' % (self.min_distance, Yaw, -1 * self.Horizontal_Angle)) # self.min_angle
                print(f"The nearest object is at a distance of {self.min_distance} m with bounding box: {self.nearest_object}")

        # cv2.imshow('Color Image', color_image)
        # cv2.waitKey(1)
    
        
            
    
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
