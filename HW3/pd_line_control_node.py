#!/usr/bin/env python

import rospy
import numpy as np
from controller import *
from geometry_msgs.msg import PointStamped, Twist

pub = rospy.Publisher('motor_twist',Twist,queue_size=1)

def callback(msg):
    global pub
    #define r to be half the size of image
    r = 320/2;
    
    kp = 1e-3
    kd = 0
    u1 = proportional(msg.point.x,r,kp)
    u2 = derivative(msg.point.x,r,kd,msg.header.stamp.to_sec())
    u = u1 + u2

    lin_speed = 0.3
    t = Twist()
    t.linear.x = lin_speed
    t.angular.z = u*0.5
    pub.publish(t)

def main():
    #Setup node
    rospy.init_node('controller',anonymous=True)
    
    rospy.Subscriber('/image/centroid',PointStamped,callback)
    rospy.spin()



if __name__ == '__main__':
    try:
        main()
    finally:
        pass

