#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Pose2D
from me416_lab.msg import MotorSpeedsStamped

class Listener:
    #Class that subscribes on the topic motor_speeds
    #Publishes to topic pose_arcs

    def __init__(self):
        rospy.Subscriber('motor_speeds', MotorSpeedsStamped, self.callback)
        global z
        z = Pose2D()
        z.x = 0
        z.y = 0
        z.theta = 0

    def callback(self,data):
        global z
        kang = 1
        klin = 1
        pub = rospy.Publisher('pose_arcs', Pose2D, queue_size=10)
        sr = data.right
        sl = data.left
        timesecs = data.header.stamp.secs
        timenow = rospy.Time.now()
        t_delta = timenow.to_sec() - timesecs
        if (sr==sl):
            z.x = z.x + (klin*(sr+sl)/2)*math.cos(z.theta)*(timenow.to_sec() - \
                  timesecs)
            z.y = z.y + (klin*(sr+sl)/2)*math.sin(z.theta)*(timenow.to_sec()- \
                  timesecs)
            z.theta = z.theta

        else:
            varx = (kang*(sr-sl)/2)*t_delta + z.theta
            z.x = ((klin/kang)*(sr+sl)/(sr-sl))*math.cos(varx) + z.x - \
                     ((klin/kang)*(sr+sl)/(sr-sl))*math.cos(z.theta)
            z.y = ((klin/kang)*(sr+sl)/(sr-sl))*math.sin(varx) + z.y - \
                     ((klin/kang)*(sr+sl)/(sr-sl))*math.sin(z.theta)
            z.theta = varx
    
        print "x = %f" %z.x
        print "y = %f"  %z.y
        print "theta = %f" %z.theta
        pub.publish(z)


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

