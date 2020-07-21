#!/usr/bin/env python

''' 
Simple node that repeats images from a compressed topic to a non-compressed one.
'''
import rospy
import numpy
import cv2
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
from image_processing import *
from geometry_msgs.msg import PointStamped


def callback(msg):
    print 'in cb'
    np_arr=np.fromstring(msg.data, np.uint8)
    img=cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
#    img=cv2.imdecode(np_arr,iscolor=CV_LOAD_IMAGE_COLOR)
    img=cv2.resize(img,(320,240))
    img=img[1:2,:]
    imgfirst=img_classify(img)
    val=int(img_centroid_horizontal(imgfirst))
    img_with_line = img_line_vertical(imgfirst,val)
    img_for_image_view=bridge.cv2_to_imgmsg(img_with_line,"bgr8")
    pub.publish(img_for_image_view)

    ps=PointStamped()
    ps.point.x=val
    time=rospy.Time.now()
    ps.header.stamp=time
    pub1.publish(ps)

if __name__ == '__main__':
    rospy.init_node('image_segment_node')
    rospy.Subscriber('raspicam_node/image/compressed', CompressedImage, callback, queue_size=1, buff_size=2**18)
    #the buff_size=2**18 avoids delays due to the queue buffer being too small for images

    pub = rospy.Publisher('/image/segmented', Image, queue_size=1)
    pub1=rospy.Publisher('/image/centroid',PointStamped, queue_size=1)
    bridge = CvBridge()
    rospy.spin()
