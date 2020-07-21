#!/usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import Pose2D

def callback1(data):
    #open a file for reading, and it automatically closes when done
    """with open('pose_euler_log.csv','r') as file_id:
        #using one of NumPy functions to load the data into an array
        data=np.genfromtxt(file_id,delimiter=',')
        #iterate over the rows
        for row in data:
            if ((row[1] != data.x) or (row[2] != data.y) or (row[3] != data.theta)): """
    timenow = rospy.Time.now()
    with open('pose_euler_log.csv','a') as file_id:
        file_id.write('%.6f, %.6f, %.6f, %.6f\n'%(timenow.to_sec(),data.x,data.y,data.theta))

def callback2(data):
    timenow = rospy.Time.now()
    with open('pose_arcs_log.csv','a') as file_id:
        file_id.write('%.6f, %.6f, %.6f, %.6f\n'%(timenow.to_sec(),data.x,data.y,data.theta))

def main():
    rospy.init_node('main',anonymous=True)
    #rospy.Subscriber('pose_arcs', Pose2D, callback1)
    rospy.Subscriber('pose_euler', Pose2D, callback1)
    rospy.Subscriber('pose_arcs', Pose2D, callback2)
    #Run until stopped
    rospy.spin()

if __name__ == '__main__':
    try:
         main()
    finally:
         pass
