#! /usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
from std_msgs.msg import Float64


class Camera(object):

    def __init__(self):

        #ROS To OpenCV Converter.
        self.bridge = CvBridge()
        self.counter = 0
        
    def get_image(self,msg):
        self.image = self.bridge.imgmsg_to_cv2(msg,"bgr8")
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
        
    if cv2.waitKey(1)%256 == 32:
        print("Image Captured and Saved")
        cam.save_image(image)

def main():
    global cam,sub,bot

    cam = Camera()

    rospy.init_node("image_node",anonymous =True)
    
    sub = rospy.Subscriber('/camera/color/image_raw', Image, callback, queue_size=10)

    rate = rospy.Rate(10)
    
    rospy.spin()
        
if __name__ == '__main__':
    try:
        main()
            
    except rospy.ROSInterruptException:
        pass