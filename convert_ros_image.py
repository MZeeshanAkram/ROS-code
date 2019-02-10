"""
                convert_ros_image.py

This script will convert ROS image and depth topics
into CV objects using 'cv_bridge' library. Then CV image
objects will be used to measure the size of object.

USAGE: Imported by ros_img_object_size.py
"""
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

rgb_topic_map = {
  1 : '/usb_cam/image_raw'
}
depth_topic_map = {
  1 : '/camera/depth/image_raw'
}


class image_converter():  

  def __init__(self):

    self.bridge = CvBridge()
    self.image_sub = None
    self.depth_sub = None
    self.cv_image = None
    self.depth_image = None
    self.img_cam_id = 0
    self.depth_cam_id = 0


  def ret_cv_img(self,topic_index):
    
    if  self.img_cam_id != topic_index:
      if self.image_sub is not None:
        self.image_sub.unregister()
      self.image_sub = rospy.Subscriber(rgb_topic_map[topic_index],Image,self.img_callback)
      self.img_cam_id = topic_index
    
    if self.cv_image is not None:
      return self.cv_image

  def ret_depth_img(self,topic_index):
    
    if  self.depth_cam_id != topic_index:
      if self.depth_sub is not None:
        self.depth_sub.unregister()
      self.depth_sub = rospy.Subscriber(depth_topic_map[topic_index],Image,self.depth_callback)
      self.depth_cam_id = topic_index
    
    if self.depth_image is not None:
      return self.depth_image

  def img_callback(self,data):

    cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    self.cv_image = cv_image

  def depth_callback(self,data):
    #print data
    depth_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
    self.depth_image = depth_image


