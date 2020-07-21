#!/usr/bin/env python

""" This node listens to the /chatter topic and responds if another node has published to it. 
Talker and Listener classes adapted from code written by Professor Roberto Tron.

Abdullah Alhashim
Noah Bernays
"""

import rospy
from std_msgs.msg import String

class Talker():
    """Class that publishes to the topic chatter"""
    def __init__(self):
        #Init publisher on the 'chatter' topic
        self.pub=rospy.Publisher('chatter', String, queue_size=10)
        rospy.Subscriber('chatter', String, self.callback)
	# This variable is used because the first message fails to be published for some reason 
	self.count = 0

	#Used a global to be able to compare the caller_id inside the listener's callback to the talker
	global name
        name = rospy.get_name()

    def callback(self,data):
        """Callback for the subscriber""" 
	response = " "
	rospy.sleep(1)

	#Make sure the node is not responding to its own messages
	if name != data._connection_header["callerid"]:
	        if data.data == "That's a stupid name.":
                	response = "That's not very nice!"
		elif data.data == "Looking for nice? Go to Disney Land.":
			response = "I've been, the bathrooms aren't too clean."
		#Without this if statement, empty strings were being published
                if response != " ":
			self.pub.publish(response)
                	rospy.loginfo(response)

    def talk(self):
        #Prepare the first message, publish, and print
	#The if statements are to circumvent some wierd order of printing we were seeing
	hello_str = " "
	if self.count < 2:
		hello_str = "Hi. My name is " + name + "."
        	self.pub.publish(hello_str)
	if self.count !=0 and hello_str != " ":
		rospy.loginfo(hello_str)

def talker():
    """Setup node and talker object. Main ROS loop."""
    #Init node. anonymous=True allows multiple launch with automatically assigned names
    rospy.init_node('talker',anonymous='True')
    #Set rate to use (in Hz)
    rate = rospy.Rate(2)
    
    #to stands for tALKER oBJECT, lo for lISTENER oBJECT
    to=Talker()
    lo = Listener()
    
    while not rospy.is_shutdown():
        #Talk
        to.talk()
	to.count += 1
        #Wait until it is done
        rate.sleep()

class Listener:
    global name

    """Class that subscribes on the topic chatter and echoes what it receives"""
    def __init__(self):
        #Use the 'chatter' topic
        rospy.Subscriber('chatter', String, self.callback)
	self.pub=rospy.Publisher('chatter', String, queue_size=10)

    def callback(self,data):
        """Callback for the subscriber"""
	response = " "
	rospy.sleep(1)

	#Make sure the node is not responding to its own messages
	if name != data._connection_header["callerid"]:
		if data.data[0:2] == "Hi":
			response = "That's a stupid name."
		elif data.data == "That's not very nice!":
                        response = "Looking for nice? Go to Disney Land."
		#Without this if statement, empty strings were being published
                if response != " ":
                        self.pub.publish(response)
                        rospy.loginfo(response)

if __name__ == '__main__':

    #Used a global to be able to compare the caller_id inside the listener's callback to the talker
    global name
    name = " "

    try:
	talker()
    finally:
        pass
