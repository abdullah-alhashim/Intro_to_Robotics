#!/usr/bin/env python

import rospy
import numpy as np
from math import pi

time_previous = 0.0000000000000001
e_previous = 0

def proportional(x,r,kp):
    u = -kp*(x-r)
    return u

def derivative(x,r,kd,time):
    global time_previous , e_previous
#    time = rospy.Time.now().to_sec()
    e = x-r
    de = (e-e_previous)/(time-time_previous)
    u = -kd*de
    #assign error and time to be previous
    e_previous = e
    time_previous = time
    return u

def main():
    #Setup node
    rospy.init_node('controller',anonymous=True)
    
    #2.3 testing the functions
#    r = np.array([[0,0,0]])
#    x = np.array([2,2,pi]) #reference/goal
    x = 3 #state
    r= 0 #reference/goal
    kp = 1 #proportional gain
    kd = 1 #derivative gain
    print 'x=%f\n r=%f\n kp=%f\n kd=%f\n'%(x,r,kp,kd)
    u1 = proportional(x,x,kp)
    print 'proportional(x,x,kp) = %f'%(u1)
    u2 = proportional(x,r,kp)
    print 'proportional(x,r,kp) = %f'%(u2)
    a=1
    print 'a=%f'%a
    derivative(x,r,kd,0)
    u3 = derivative(x+a,r+a,kd,1)
    print 'derivative(x+a,r+a,kd,1) = %f'%(u3)
    u4 = derivative(x,r,1,0) 
    u4 = derivative(x,r+a,1,1)
    print 'derivative(x,r+a,1,1) = %f'%(u4)

if __name__ == '__main__':
    try:
        main()
    finally:
        pass

