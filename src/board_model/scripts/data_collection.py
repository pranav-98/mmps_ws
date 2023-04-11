#! /usr/bin/env python

import rospy
import cv2
import keyboard 
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
from std_msgs.msg import Float64

class Mobbot(object):
    def __init__(self):
        #Publish Torques on this topics
        self.REAR_LEFT_WHEEL = "/skateboard_test/joint1_effort_controller/command"
        self.FRONT_LEFT_WHEEL = "/skateboard_test/joint2_effort_controller/command"
        self.REAR_RIGHT_WHEEL = "/skateboard_test/joint3_effort_controller/command"
        self.FRONT_RIGHT_WHEEL = "/skateboard_test/joint4_effort_controller/command"
        
        #Create a ROS Publishers.
        self.pub_1 = rospy.Publisher(self.REAR_LEFT_WHEEL,Float64,queue_size=1)
        self.pub_2 = rospy.Publisher(self.FRONT_LEFT_WHEEL,Float64,queue_size=1)
        self.pub_3 = rospy.Publisher(self.REAR_RIGHT_WHEEL,Float64,queue_size=1)
        self.pub_4 = rospy.Publisher(self.FRONT_RIGHT_WHEEL,Float64,queue_size=1)
        
    def move(self)->None:
        if keyboard.read_key() == "w":
            
            self.pub_1.publish(1.0)
            self.pub_2.publish(1.0)
            self.pub_3.publish(1.0)
            self.pub_4.publish(1.0)
        
        elif(keyboard.read_key()=="a"):
            
            self.pub_1.publish(1.0)
            self.pub_2.publish(1.0)
            self.pub_3.publish(-1.0)
            self.pub_4.publish(-1.0)
        
        elif(keyboard.read_key()== "d"):
            self.pub_1.publish(-1.0)
            self.pub_2.publish(-1.0)
            self.pub_3.publish(1.0)
            self.pub_4.publish(1.0)
        
        elif(keyboard.read_key()== "s"):
            self.pub_1.publish(0.0)
            self.pub_2.publish(0.0)
            self.pub_3.publish(0.0)
            self.pub_4.publish(0.0)
        
        else:
            print("Unknown Input")
    
    def __del__(self):
        print("MMBOT Object deleted")
    
        
class Camera(object):

    def __init__(self):

        #ROS To OpenCV Converter.
        self.bridge = CvBridge()
        self.counter = 0
        
    def get_image(self,msg):
        self.image = self.bridge.imgmsg_to_cv2(msg,"passthrough")
        return self.image
    
    @staticmethod
    def show_image(image):
        cv2.imshow('Image',image)
        cv2.waitKey(1)

    def crop_image(self,image):
        image = image[self.x:self.y, self.w:self.h]
        return image
    
    def save_image(self,img):
        self.counter += 1
        cv2.imwrite("/home/varun/mmps_ws/src/board_model/data/img" + str(self.counter) + ".jpg",img)


def callback(msg):

    image = cam.get_image(msg)
    #depth_image = cam.crop_image(image)
    
    cam.show_image(image)
    
    bot.move()
    
    if cv2.waitKey(1)%256 == 32:
        print("Image Captured and Saved")
        cam.save_image(image)

def main():
    global cam,sub,bot

    cam = Camera()
    bot = Mobbot()
    
    rospy.init_node("image_node",anonymous =True)
    
    sub = rospy.Subscriber('/kinect/depth/image_raw', Image, callback, queue_size=10)

    rate = rospy.Rate(10)
    
    rospy.spin()
        
if __name__ == '__main__':
    try:
        main()
            
    except rospy.ROSInterruptException:
        pass