#!/usr/bin/env python

"""This node subscribes to the \motor_twist and translates commands into actual robot motion.

Abdullah Alhashim
Noah Bernays
"""

import rospy
import me416_utilities as mu
from geometry_msgs.msg import Twist

class Listener:
    #Class that subscribes on the topic \motor_twist and sets the motors appropriately based on the received Twist message

    def __init__(self):
        #Use the 'motor_twist' topic
        rospy.Subscriber('motor_twist', Twist, self.callback)
    
    #Change this speed_offset if the robot is turning while both motors are set to the same value
	self.speed_offset = 1
	#Create two objects from the classes MotorSpeedLeft and MotorSpeedRight which exist in me416_utilities
	self.L_motor=mu.MotorSpeedLeft()
        self.R_motor=mu.MotorSpeedRight(self.speed_offset)

	#To adjust the variables before actually setting the motors
	self.setRight = 0
	self.setLeft = 0

    def callback(self,data):

	#Set both motors to linear command
        self.setRight = data.linear.x
        self.setLeft = data.linear.x

	#Incorporate angular data
	if data.angular.z > 0:
		self.setRight += data.angular.z
	if data.angular.z < 0:
		self.setLeft -= data.angular.z

	""" #This works, it's just a little choppier than the algorithm we came up with
	k_linear = float(1)
	k_angular = float(0.5)
	self.setLeft = data.linear.x / k_linear - data.angular.z / k_angular
	self.setRight = data.linear.x / k_linear + data.angular.z / k_angular
	"""

	#Before setting the motors, make sure the commands are between 1 and -1
	if self.setLeft > 1:
        	self.setLeft = 1
        if self.setLeft < -1:
        	self.setLeft = -1
        if self.setRight > 1:
        	self.setRight = 1
        if self.setRight < -1:
        	self.setRight = -1

	#Set the motor speeds
	self.L_motor.set_speed(self.setLeft)
	self.R_motor.set_speed(self.setRight)

	#Print what each motor is set to
        rospy.loginfo("L_motor set to: " + str(self.setLeft))
	rospy.loginfo("R_motor set to: " + str(self.setRight))

def listener():
    #Setup node
    rospy.init_node('listener',anonymous=True)
    #Create the listener object
    lo=Listener()
    #Run until stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    finally:
        pass
