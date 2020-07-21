#!/usr/bin/env python

import rospy
import me416_utilities as mu
import numpy as np
from math import cos, sin
from me416_lab.msg import MotorSpeedsStamped
from geometry_msgs.msg import Pose2D

"""

Abdullah Alhashim
Nicole Calero
"""

class Euler_integration:
    def __init__(self):
        self.z_k = np.array([[0],[0],[0]])
        self.z_kp1 = np.array([[0],[0],[0]])
        self.klin = 1.0
        self.kang = 1.0
        self.A = np.array([[(self.klin/2)*cos(self.z_k[2]) , (self.klin/2)*cos(self.z_k[2])],
             [(self.klin/2)*sin(self.z_k[2]) , (self.klin/2)*sin(self.z_k[2])],
             [-self.kang/2 , self.kang/2]])
	self.motor_speeds_last_received = np.array([[0],[0]])
        self.tstamp_kp1 = rospy.Time.now()
        self.tstamp_k = rospy.Time.now()
        self.pose_msg = Pose2D()
        rospy.Subscriber('motor_speeds', MotorSpeedsStamped, self.callback)
        self.pub = rospy.Publisher('pose_euler', Pose2D, queue_size=10)

    def callback(self,data): #this call back updates the last received motor speeds
        self.motor_speeds_last_received = np.array([[data.left],[data.right]])

        #self.z_k = np.array([data.left,data.right,z_k[2]]) #theta=z_k[2] ?
        self.tstamp_k = data.header.stamp

	#print "x = %f" %self.z_kp1[0]
	#print "y = %f"  %self.z_kp1[1]
	#print "theta = %f" %self.z_kp1[2]

    def update_state(self):
        # this function updates and publishes the state of the robot using the last recieved speeds

	# update A matrix
        self.A = np.array([[(self.klin/2)*cos(self.z_k[2]) , (self.klin/2)*cos(self.z_k[2])],
             [(self.klin/2)*sin(self.z_k[2]) , (self.klin/2)*sin(self.z_k[2])],
             [-self.kang/2 , self.kang/2]])

        self.tstamp_kp1 = rospy.Time.now()
        # apply Euler's Integration
        self.z_kp1 = self.z_k + self.A.dot(self.motor_speeds_last_received) * (self.tstamp_kp1.to_sec() - self.tstamp_k.to_sec())
        # (self.tstamp_kp1 - self.tstamp_k) might need to be converted to seconds

        # construct the Pose2D message
        self.pose_msg.x = self.z_kp1[0]
        self.pose_msg.y = self.z_kp1[1]
        self.pose_msg.theta = self.z_kp1[2]

	print "x = %f" %self.z_kp1[0]
	print "y = %f"  %self.z_kp1[1]
	print "theta = %f" %self.z_kp1[2]
#	print self.A
        # publish Pose2D message (robot state)
        self.pub.publish(self.pose_msg)

        # update previous state to the new state, and store the time now to be used as t_k+1
        self.z_k = self.z_kp1
	self.tstamp_k = self.tstamp_kp1

def odometry_wheel_euler():
    #Init node
    rospy.init_node('odometry_wheel_euler',anonymous='True')

    #create Euler integration object
    EI = Euler_integration()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        EI.update_state()
        rate.sleep()


if __name__ == '__main__':
    try:
        odometry_wheel_euler()
    finally:
        pass
