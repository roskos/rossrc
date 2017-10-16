#!/usr/bin/env python2
import rospy
import rosbag
import time
from mavros_msgs.srv import *
from mavros_msgs.msg import ActuatorControl
from std_msgs.msg import Header
from std_msgs.msg import Float64

rospy.init_node('test_node', anonymous=True)
pub_act = rospy.Publisher('/mavros/actuator_control', ActuatorControl, queue_size=10)
rate = rospy.Rate(1000)

rospy.wait_for_service('/mavros/cmd/arming')
try:
	armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
	armService(True)
except rospy.ServiceException, e:
	print "Service arm call failed: %s"%e

rospy.wait_for_service('/mavros/set_mode')
try:
	flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
	#http://wiki.ros.org/mavros/CustomModes for custom modes
	isModeChanged = flightModeService(custom_mode='OFFBOARD') #return true or false
except rospy.ServiceException, e:
	print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e

act = ActuatorControl()
act.header = Header()
act.controls[0] = 0.0 #ros_roll
act.controls[1] = 0.0 #ros_pitch
act.controls[2] = 0.0 + 0.2#ros_yaw+offset
act.controls[3] = 0.0 #ros_throttle
act.controls[4] = 0.0
act.controls[5] = 0.0
act.controls[6] = 0.0
act.controls[7] = 0.0


while not rospy.is_shutdown():
	pub_act.publish(act)
	act.controls[2] = 0.0 + 0.2#ros_yaw+offset
	act.controls[3] = 0.5 #ros_throttle
rate.sleep()
