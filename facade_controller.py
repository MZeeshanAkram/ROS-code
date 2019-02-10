#!/usr/bin/env python
"""
                facade_controller.py

This script will stream video frames in browser.
It will receive JPEG image frames from 
'convert_ros_image_to_jpeg.py' and will send to the browser.
It will stream video data of multiple cameras. 
"""

from __future__ import print_function

from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
import json

from flask import Flask, render_template, Response
from convert_ros_image import image_converter
import rospy


app = Flask(__name__)
CORS(app)
api = Api(app)

rospy.init_node('image_converter', anonymous=True)

class Streaming(Resource):

    def __init__(self):

        self.image_converter = image_converter()


    def get(self,cam_id):

        return self.video_feed(cam_id)


    def gen(self,cam_id):

        while True:
            frame = self.image_converter.ret_jpeg_img(cam_id)

            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


    def video_feed(self,cam_id):

        return Response(self.gen(cam_id), mimetype='multipart/x-mixed-replace; boundary=frame')



api.add_resource(Streaming, '/Streaming/<int:cam_id>')


if __name__ == '__main__':
    
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, threaded=True)


