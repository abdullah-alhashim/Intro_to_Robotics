#!/usr/bin/env python
#

import rospy
import me416_utilities as mu
from geometry_msgs.msg import Twist

class Key_Commander():
    def __init__(self):
	self.pub=rospy.Publisher('motor_twist', Twist, queue_size=10) #making this node a publisher
	self.msg=Twist()
	self.msg.linear.x=0	#initializing the speed parameters
	self.msg.angular.z=0
    def send(self):
        getch = mu._Getch()  #Runs to recieve key commands
	rate = rospy.Rate(50)
	speed_linear = self.msg.linear.x  #setting up variables specified in HW
	speed_angular = self.msg.angular.z
        while  not rospy.is_shutdown():
            key = getch()
	#Runs through all the possibilities for key commands and prints
            if key == 'w':
	        if speed_linear < 1.0:
		    speed_linear=speed_linear + 0.2   #increasing linear speed by 0.2
	            rospy.loginfo("New linear speed is %0.1f",speed_linear)
	        else:
		    rospy.loginfo("Linear speed is already at maximum, 1.0.")
	    elif key == 's':
	        if speed_linear > -1.0:
		    speed_linear=speed_linear - 0.2   #decreasing linear speed by 0.2
	            rospy.loginfo("New linear speed is %0.1f",speed_linear)
	        else:
		    rospy.loginfo("Linear speed is already at minimum, -1.0.")
            elif key == 'd':
	        if speed_angular < 1.0:
		    speed_angular = speed_angular + 0.2  #increasing angular speed by 0.2
                    rospy.loginfo("New angular  speed is %0.1f",speed_angular )
	        else:
		    rospy.loginfo("Angular speed is already at maximum, 1.0.")
	    elif key == 'a':
	        if speed_angular > -1.0:
		    speed_angular = speed_angular -0.2  #decreasing angular speed by 0.2
                    rospy.loginfo("New angular speed is %0.1f",speed_angular )
                else: 
		    rospy.loginfo("Angular speed is already at minimum, -1.0.")
	    elif key == 'q':
		rospy.loginfo("Shutdown initiated")
		rospy.signal_shutdown("Shutting down initiated by key_emergency_switch")
	    else:
	        pass 
	#Need to spend the values of the variables back to Twist
	    self.msg.linear.x = speed_linear   
	    self.msg.angular.z = speed_angular
            self.pub.publish(self.msg)  #sends back to Twist
	    rate.sleep()
#initialized the node
def key_op():
    rospy.init_node('Key_Commander')
    rate = rospy.Rate(1)
    zo = Key_Commander()
    print("Press 'w' to increase linear speed.\n Press 's' to decrease linear speed.\n Press 'd' to increase angular speed.\n  Press 'a' to decrease angular speed. ")
    while not rospy.is_shutdown():
	zo.send()
	rate.sleep()
 
if __name__ == '__main__':
    try:
        key_op()
    finally:
        pass
