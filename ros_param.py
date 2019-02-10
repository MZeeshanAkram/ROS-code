"""
				ros_param.py

python script that will load ROS Parameters 
from a YAML file, parse them and will upload
them to ROS 'Parametr Server'. 
"""

import rospy
import rosparam 
import yaml

with open("validation_params.yaml", 'r') as stream:
    data = yaml.load(stream)

while len(data)>0:
    parameter = data.popitem()
    rosparam.set_param(parameter[0],str(parameter[1]))
