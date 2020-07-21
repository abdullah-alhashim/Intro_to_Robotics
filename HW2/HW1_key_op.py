#!/usr/bin/env python

import rospy
import me416_utilities as mu
from geometry_msgs.msg import Twist

""" This node listens for keyboard commands and updates the speed_linear
and speed_angular values accordingly, then publishes the Twist data to the
/motor_twist topic
 Control-c does not kill this node: you need to type "rosnode list" to find the name of the node,
and then type "rosnode kill <node_name>" in another terminal

Abdullah Alhashim
Noah Bernays
"""

class TwistCommand():
    #Class that prepares and publishes a Twist message of the linear and angular speeds based on which keys were pressed
    def __init__(self):
        #Init publisher on the 'chatter' topic
        self.pub = rospy.Publisher('motor_twist', Twist, queue_size=10)
        self.speed_linear = 0
	self.speed_angular = 0
	self.SPEED_DELTA = 0.2

    def update(self, key):

	global twist_msg

	update = 0

	#Increment the appropriate field given which key was pressed
        if key == 'w':
		self.speed_linear += self.SPEED_DELTA
		update = 1
	if key == 's':
		self.speed_linear -= self.SPEED_DELTA
		update = 1
	if key == 'd':
		self.speed_angular += self.SPEED_DELTA
		update = 1
	if key == 'a':
		self.speed_angular -= self.SPEED_DELTA
		update = 1

	#No need to do anything if nothing was updated
	if update == 1:
		#make sure linear speeds are between 0.4 and -0.4
		#and angular speeds between 0.6 and -0.6 before publishing
		#to allow for turning at "max" speed
		if self.speed_linear > 0.4:
			self.speed_linear = 0.4
		if self.speed_linear < -0.4:
                	self.speed_linear = -0.4
		if self.speed_angular > 0.6:
                	self.speed_angular = 0.6
		if self.speed_angular < -0.6:
                	self.speed_angular = -0.6

		#Print the updated speeds
		rospy.loginfo("Updated speed_linear = " + str(self.speed_linear))
		rospy.loginfo("Updated speed_angular = " + str(self.speed_angular))

		#Prepare Twist message
		twist_msg.linear.x = self.speed_linear
		twist_msg.angular.z = self.speed_angular

        	#Publish
        	self.pub.publish(twist_msg)

def key_op():
    #Function that continuously checks for key presses

    """Setup node and twistCommand object. Main ROS loop."""
    #Init node. anonymous=True allows multiple launch with automatically assigned names
    rospy.init_node('key_command',anonymous='True')
    #Set rate to use (in Hz)
    rate = rospy.Rate(50)

    #to stands for tWISTcOMMAND oBJECT
    tco = TwistCommand()

    #Print out directions and current speeds
    command_info = "'w': increment speed_linear;\n's': decrement speed_linear;\n'd': increment speed_angular;\n'a': decrement speed_angular"
    rospy.loginfo(command_info)
    rospy.loginfo("Current speed_linear: " + str(tco.speed_linear))
    rospy.loginfo("Current speed_angular: " + str(tco.speed_angular))

    global twist_msg
    twist_msg = Twist()

    #Boilerplate to get function to read keyboard
    getch = mu._Getch()

    while not rospy.is_shutdown():
        #check for keyboard commands
	key = getch()
        tco.update(key)
        #Wait until it is done
        rate.sleep()

if __name__ == '__main__':
    try:
        key_op()
    finally:
        pass
