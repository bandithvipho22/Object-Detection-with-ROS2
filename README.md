# Objective
The primary objective of this project is to participate in the ABU Robocon Competition by performing object detection (system) to identify blue and red balls. It will allow a robot to complete challenges autonomously under the rules of the competition.

![image](https://github.com/user-attachments/assets/53473a15-916c-4e06-b24f-91d6371683a4)

# Requirement:
In this project, we implemented on the Jetson AGX Xavier using the RealSense D435i.
+ Jetson Flashing (Ubuntu 20.04):
  + Jetpack 5.1.2 buit-in Libraries,
  + CUDA: 11.4.315,
  + TensorRT: 8.5.2.2
  + CuDNN: 8.6.0.166,
  + OpenCV: 4.5.4
+ Setup YOLO Model on Jetson AGX Xavier:
  + Setup Realsense for Jetson Packages
  + Ultralytics: 8.2.16 (Remove torch and torchvision)
  + Re-Install pytorch and torchvision (Available with JP 5.1.2)
  + Setup onnx for tensor RT conversion
  
![image](https://github.com/user-attachments/assets/6b9b9117-2216-449b-bacc-f67eb52cabc6)

# Results
After, setup the yolo model on the hardware we get the result from the both frames of Realsense D435i and Webcam on the Robot MR2:

## Command
To run the code for object detection, there are 2 codes:
### 1). Object Detection with Webcam
```
python3 yolov8_webcam.py
```
![image](https://github.com/user-attachments/assets/6cdd9f89-618d-4182-9b6f-fdcfb163f9ee)

### 2). Object Detection with Realsense D435i
+ There are several function:
  + Detect color of ball
  + Publish Distance of ball
  + Couting ball
  + Publish min angle and min distance (Robot's be alble to know the nearest ball)

```
python3 yolov8_rs07.py
```
![image](https://github.com/user-attachments/assets/e364f401-5168-4c68-bf47-5686191615ff)

Note that: If you want more detail on this project you could go to folder "Documents" and read my Slide or Report
