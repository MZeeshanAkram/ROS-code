#!/usr/bin/env python

import sys
import rospy
from sensor_stream_validation.srv import *
from std_srvs.srv import Empty

def hz_monitoring_client(x, y, a, b):
    rospy.wait_for_service('monitor_hz')
    try:
        monitor_hz = rospy.ServiceProxy('monitor_hz', timeSync)
        response = monitor_hz(x, y, a, b)
        return response.srv_response
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.arg`v[0]

if __name__ == "__main__":
    if len(sys.argv) == 5:
        x = " ".join(sys.argv[1])
        y = " ".join(sys.argv[2])
        x1 = int(sys.argv[3])
        y1 = int(sys.argv[4])
    else:
        print usage()
        sys.exit(1)
    print "Requesting s"
    print ("client ", hz_monitoring_client(x, y,x1,y1))