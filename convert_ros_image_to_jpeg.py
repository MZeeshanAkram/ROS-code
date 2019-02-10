"""
                convert_ros_image_to_jpeg.py

This script will convert ROS image topic into
CV image object using 'cv_bridge' library.
Then CV image object will be converted JPEG image
frames which will be used for streaming.

USAGE: Imported in 'facade_controller.py'
"""
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

topic_map = {
  1 : '/usb_cam/image_raw'
}


class image_converter():  

  def __init__(self):

    self.bridge = CvBridge()
    self.image_sub = None
    self.cv_image = None
    self.cam_id = 0

  def ret_jpeg_img(self,topic_index):

    if  self.cam_id != topic_index:
      if self.image_sub is not None:
        self.image_sub.unregister()
      self.image_sub = rospy.Subscriber(topic_map[topic_index],Image,self.callback)
      self.cam_id = topic_index

    if self.cv_image is not None:

      ret, jpeg = cv2.imencode('.jpg',self.cv_image)
      out_img = jpeg.tobytes()
      return out_img


  def callback(self,data):

    cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    self.cv_image = cv_image

