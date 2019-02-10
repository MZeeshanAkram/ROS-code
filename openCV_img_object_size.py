#!/usr/bin/env pytnhon
# USAGE
# python distance_to_camera.py

# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
from convert_ros_image import image_converter
import rospy
import numpy as np

#from cv_bridge import CvBridge, CvBridgeError

def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)

	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)

	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)

def object_size(knownDepth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownDepth * perWidth) / focalLength

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 0.3

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
#KNOWN_WIDTH = 5.0

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length

focalLength = 760.0


class undistort:

	def __init__(self):
	
		self.mtx = np.array([[639.173769, 0.000000, 275.061764], [0.000000, 638.682629, 228.912752], [0.000000, 0.000000, 1.000000]])
		self.dist = np.array([[-0.144163, -0.146376, -0.001392, -0.013187, 0.000000]])
		
	def rectify(self,img):
		h, w = img.shape[:2]
		print(h,w)
		newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),1,(w,h))

		dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
		# crop the image
		x,y,w,h = roi
		dst = dst[y:y+h, x:x+w]
		return dst
#####################
#initialize 'undistort'
undistort = undistort()
# loop over the images
cap = cv2.VideoCapture(0)
print"capture object"

while True:
	#print "here\n"
	ret, image= cap.read()
	if image is not None:
		
	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera
		image = undistort.rectify(image)
		marker = find_marker(image)
		inches = object_size(KNOWN_DISTANCE, focalLength, marker[1][0])
		print(inches," METERS WIDE")
		# draw a bounding box around the image and display it
		box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
		box = np.int0(box)
		#cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
		#cv2.putText(image, "%.4fM" % (inches / 12),
		#	(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		#	2.0, (0, 255, 0), 3)

		cv2.imshow("image", image)

		if (cv2.waitKey(1) & 0xFF) == ord('q'):
			break

								
cap.release()
cv2.destroyAllWindows()