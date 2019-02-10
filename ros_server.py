#!/usr/bin/env python

import rospy
from sensor_stream_validation.srv import timeSync
from std_srvs.srv import Empty

def handle_hz_monitoring(req):
    print "Returning "
    return 1

def hz_monitoring_server():
    rospy.init_node('hz_monitoring_server')
    s = rospy.Service('monitor_hz', timeSync, handle_hz_monitoring)
    print "Ready."
    rospy.spin()

if __name__ == "__main__":
    hz_monitoring_server()