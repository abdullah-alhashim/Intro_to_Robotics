#!/usr/bin/env python

import rospy
import numpy as np
import cv2
from sensor_msgs import Image, RegionOfInterest


"""
Hackathon 3

Abdullah Alhashim
"""

class face_detection:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        rospy.Subscriber('/raspicam_node/image/Compressed', CompressedImage, self.callback)
        self.image = rospy.Publisher('/face_detection/image', Image, queue_size=10)
        self.boxes_image = rospy.Publisher('/face_detection/boxes_image', Image, queue_size=10)
        self.boxes = rospy.Publisher('/face_detection/boxes', RegionOfInterest, queue_size=10)

    def callback(self,data):
        #img = cv2.imread()
        print 'in callback'


def hackathon_3():
    #Init node
    rospy.init_node('face_detection',anonymous='True')

    #create Euler integration object
    fd = face_detection()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        EI.update_state()
        rate.sleep()


if __name__ == '__main__':
    try:
        hackathon_3()
    finally:
        pass
