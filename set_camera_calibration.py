#!/usr/bin/env python
import rospy
#from sensor_msgs.msg import CameraInfoManager 
from camera_info_manager_py import CameraInfoManager
#from camera_info_manager_py import CameraInfoError

rospy.init_node('image_calibrator', anonymous=True)
camera = CameraInfoManager(cname='head_camera',url='file:///home/zeeshan/.ros/camera_info/head_camera.yaml',namespace='front')

camera.loadCameraInfo()
print camera.getCameraInfo()
'''
if camera.isCalibrated():
	print(1)
print(1)
'''
rospy.spin()
