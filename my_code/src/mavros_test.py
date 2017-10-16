#!/usr/bin/env python
import rospy
import rosbag
import time
from std_msgs.msg import String, Header
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from geometry_msgs.msg import TwistStamped
from mavros_msgs.msg import ActuatorControl
from std_msgs.msg import Float64


#global variable
latitude =0.0
longitude=0.0

pub_act = rospy.Publisher('/mavros/actuator_control', ActuatorControl, queue_size=10)


def setGuidedMode():
	rospy.wait_for_service('/mavros/set_mode')
	try:
		flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
		#http://wiki.ros.org/mavros/CustomModes for custom modes
		isModeChanged = flightModeService(custom_mode='OFFBOARD') #return true or false
	except rospy.ServiceException, e:
		print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e


def setStabilizeMode():
	rospy.wait_for_service('/mavros/set_mode')
	try:
		flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
		#http://wiki.ros.org/mavros/CustomModes for custom modes
		isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
	except rospy.ServiceException, e:
		print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e


def setLandMode():
	rospy.wait_for_service('/mavros/cmd/land')
	try:
		landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
		#http://wiki.ros.org/mavros/CustomModes for custom modes
		isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
	except rospy.ServiceException, e:
		print "service land call failed: %s. The vehicle cannot land "%e


def setArm():
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(True)
	except rospy.ServiceException, e:
		print "Service arm call failed: %s"%e


def setDisarm():
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(False)
	except rospy.ServiceException, e:
		print "Service arm call failed: %s"%e




def setTakeoffMode():
	rospy.wait_for_service('/mavros/cmd/takeoff')
	try:
		takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL)
		takeoffService(altitude = 2, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
	except rospy.ServiceException, e:
		print "Service takeoff call failed: %s"%e






def globalPositionCallback(globalPositionCallback):
	global latitude
	global longitude
	latitude = globalPositionCallback.latitude
	longitude = globalPositionCallback.longitude
	#print ("longitude: %.7f" %longitude)
	#print ("latitude: %.7f" %latitude)


def my_code():
	act = ActuatorControl()
	act.header = Header()
	act.controls[0] = 0.0 #ros_roll
	act.controls[1] = 0.0 #ros_pitch
	act.controls[2] = 1 #ros_yaw
	act.controls[3] = 0.5 #ros_throttle
	act.controls[4] = 0.0
	act.controls[5] = 0.0
	act.controls[6] = 0.0
	act.controls[7] = 0.0
	
	while not rospy.is_shutdown():
		pub_act.publish(act)


def menu():
	print "Press"
	print "1: to set mode to GUIDED"
	print "2: to set mode to STABILIZE"
	print "3: to set mode to ARM the drone"
	print "4: to set mode to DISARM the drone"
	print "5: to set mode to TAKEOFF"
	print "6: to set mode to LAND"
	print "7: print GPS coordinates"
	print "8: run my code"




def myLoop():
	x='1'
	while ((not rospy.is_shutdown())and (x in ['1','2','3','4','5','6','7'])):
		menu()
		x = raw_input("Enter your input: ");
		if (x=='1'):
			setGuidedMode()
		elif(x=='2'):
			setStabilizeMode()
		elif(x=='3'):
			setArm()
		elif(x=='4'):
			setDisarm()
		elif(x=='5'):
			setTakeoffMode()
		elif(x=='6'):
			setLandMode()
		elif(x=='7'):
			global latitude
			global longitude
			print ("longitude: %.7f" %longitude)
			print ("latitude: %.7f" %latitude)
		elif(x=='8'):
			my_code()
		else:
			print "Exit"








if __name__ == '__main__':
	rospy.init_node('my_mav', anonymous=True)
	rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)
	velocity_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
	pub_act = rospy.Publisher('/mavros/actuator_control', ActuatorControl, queue_size=10)
	act = ActuatorControl()
	# spin() simply keeps python from exiting until this node is stopped


	#listener()
	myLoop()
	#rospy.spin()
