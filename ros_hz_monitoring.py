"""
                ros_hz_monitoring.py

This script will monitor the frequency of all the 
Subscribed topics and will generate warning if HZ
of any topic drop below the desired rate. 

The list of all the topics will be provided in the 
'topic_list' variable while desired hz values will 
be recieved from ros 'Parameter Server'.
"""

#!/usr/bin/env python
import rospy
import time
import sensor_msgs.msg 
from sensor_msgs.msg import PointCloud2,Imu,Image,NavSatFix
import numpy as np
import rosparam 

topic_list = ['/camera/depth/image_raw_front','/iqbal/imu/data','/iqbal/navsat/fix']

class timeSync_Verification:

    def __init__(self, listener_node, topic_names ):
        self.listener_node = listener_node
        rospy.init_node(self.listener_node)
        self.avg_array = [[0 for x in range(200)] for y in range(3)] 
        self.topic_names = topic_names
        self.first = 0.0
        #   Subscriber for each topic
        rospy.Subscriber(topic_names[0],Image,self.handler,0)
        rospy.Subscriber(topic_names[1],Imu,self.handler,1)
        rospy.Subscriber(topic_names[2],NavSatFix,self.handler,2)

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

    def handler(self,data,args):

        second = time.time()
        #second = rospy.get_time()
        self.avg_array[args]= [second-self.first]+self.avg_array[args]
        N = len(self.avg_array[args])

        # np.convolve used for calculating moving average of hertz
        freq = 1/(np.convolve(self.avg_array[args], np.ones((N,))/N, mode='valid'))[0]
        
        # starts evaluating HZ once 'avg_array' is completely full.
        if self.avg_array[args][-1] != 0.0:

            desired_parameter = rosparam.get_param(self.topic_names[args]+'/timeSync')

            if freq <= desired_parameter-0.1*desired_parameter or freq >= desired_parameter+0.1*desired_parameter:
                print("topic: '"+str(self.topic_names[args])+"' delayed")
            else:
                print("on time")

        self.avg_array[args].pop() 
        self.first = second


if __name__ == '__main__':
    ts = timeSync_Verification('listener',topic_list)