#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
import cv2
from std_msgs.msg import Int8
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from image_process.msg import BoundingBoxes,BoundingBox
import numpy as np

xmin = 0
xmax = 0
ymin = 0
ymax = 0
rospy.init_node('img_subscriber', anonymous=True)
r = rospy.Rate(0.1)

def imageCallback(data):
    bridge = CvBridge()
    global xmin
    global ymin
    global xmax
    global ymax
    print xmax-xmin
    print ymax-ymin
    try:
	cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
	image = cv_image[ymin:ymax,xmin:xmax]
	cv2.imwrite("person.png", image)
    except CvBridgeError as e:
      print(e)

    

def callback_bounding_boxes(data):
    for i in data.boundingBoxes:
    	if i.Class == "person":
           global xmin
      	   global ymin
	   global xmax
	   global ymax
	   xmin = i.xmin
     	   ymin = i.ymin
	   xmax = i.xmax
	   ymax = i.ymax
	   rospy.Subscriber("/zed/rgb/image_raw_color", Image, imageCallback)

def mainloop():
    rospy.init_node('img_subscriber', anonymous=True)
    rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, callback_bounding_boxes)
    rospy.spin()

if __name__ == '__main__':
    mainloop()
