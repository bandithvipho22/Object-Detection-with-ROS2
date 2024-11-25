from setuptools import setup

package_name = 'mr2_realsense'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jsagx-6',
    maintainer_email='jsagx-6@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'realsense_pub = mr2_realsense.realsense_pub_image:main',
              'realsense_pub02 = mr2_realsense.realsense_pub_image02:main',
              'yolo_pub_8 = mr2_realsense.test_opencv_8_pub:main',
              'realsense_depth = mr2_realsense.realsense_depth:main',
              'webcam_pub = mr2_realsense.webcam_pub:main',
            #   'realsense_pointcloud = cv_test.realsense_pointcloud:main',
              'yolo_ball_pub = mr2_realsense.yolo_ball_pub:main',
              'yolo_ball_pub02 = mr2_realsense.yolo_ball_pub02:main',
              'yolov8_rs = mr2_realsense.yolov8_rs:main',
 	      'yolov8_rs03 = mr2_realsense.yolov8_rs03:main',
          'yolov8_rs04 = mr2_realsense.yolov8_rs04:main',
          'yolov8_rs05 = mr2_realsense.yolov8_rs05:main',
          'yolov8_rs06 = mr2_realsense.yolov8_rs06:main',
          'yolov8_rs07 = mr2_realsense.yolov8_rs07:main',
          'yolov8_rsweb1 = mr2_realsense.yolov8_rsweb01:main',
 	      'yolov8_webcam = mr2_realsense.yolov8_webcam:main'
        ],
    },
)
