#!/usr/bin/env python
"""
This script will measure the size objects 
present in image.

USAGE: python ros_img_object_size.py
"""

# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
from convert_ros_image import image_converter
import rospy
import numpy as np

from yolo import WeightReader
import yolo
import sys

def object_size(knownDepth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownDepth * perWidth) / focalLength

KNOWN_DISTANCE = 0.0


focalLength = 548.57

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# INITIALIZE IMAGE CONVERTER NODE AND CLASS		
rospy.init_node('image_converter', anonymous=True)
image_converter = image_converter()

# Start usb_cam
cap = cv2.VideoCapture(0)

weight_reader = WeightReader()
model = crete_model(weight_reader)

while True:

	ret, image= cap.read()
	depth = image_converter.ret_depth_img(1)
	#print depth

	if image is not None:

		input_image = cv2.resize(image, (416, 416))
		input_image = input_image / 255.
		input_image = input_image[:,:,::-1]
		input_image = np.expand_dims(input_image, 0)

		netout = model.predict(input_image)
		image_, markers = interpret_netout(image, netout[0])



	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera

		
		#markers = find_marker(image)

		if depth is not None:

			for eachObject in markers: 

				(x1,x2,y1,y2) = eachObject
				object_depth_mat = depth[x1:x2,y1:y2]

		
				KNOWN_DISTANCE = np.mean(object_depth_mat)
				print ("distance",KNOWN_DISTANCE)
				# returns Width in milimeter
				Width = object_size(KNOWN_DISTANCE, focalLength, x2-x1)
				print(Width/10," centimeters")
				# returns Length in milimeter
				Length = object_size(KNOWN_DISTANCE, focalLength, y2-y1)
				print(Length/10," centimeters")
			
		
				box = cv2.cv.BoxPoints(eachObject) if imutils.is_cv2() else cv2.boxPoints(eachObject)
				box = np.int0(box)
				cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	
				(tl, tr, br, bl) = box
				(blbrX, blbrY) = midpoint(bl, br)
				(tltrX, tltrY) = midpoint(tl, tr)
				
				cv2.putText(orig, "{:.2f}cm".format(Width/10),
				(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (255, 255, 255), 2)

				cv2.putText(orig, "{:.2f}cm".format(Length/10),
				(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (255, 255, 255), 2)
			
				cv2.putText(image, "%.2fm" % (KNOWN_DISTANCE/1000),
					(tltrX+tltrY, blbrX+blbrY), cv2.FONT_HERSHEY_SIMPLEX,
										2.0, (0, 255, 0), 3)
									
				cv2.imshow("image", image)
				if (cv2.waitKey(1) & 0xFF) == ord('q'):
					break

								
cap.release()
cv2.destroyAllWindows()