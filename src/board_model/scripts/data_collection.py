#! /usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float64
import pygame
import sys

class Camera(object):
    def __init__(self):
        self.bridge = CvBridge()
        self.counter = 0

    def get_image(self, msg):
        self.image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        return self.image

    @staticmethod
    def show_image(image):
        cv2.imshow('Image', image)
        cv2.waitKey(1)

    def save_image(self, img):
        self.counter += 1
        cv2.imwrite("/home/varun/mmps_ws/src/board_model/data/img" + str(self.counter) + ".jpg", img)

class Robot(object):
    def __init__(self):
        self.pub1 = rospy.Publisher('/skateboard_test/joint1_effort_controller/command', Float64, queue_size=10)
        self.pub2 = rospy.Publisher('/skateboard_test/joint2_effort_controller/command', Float64, queue_size=10)
        self.pub3 = rospy.Publisher('/skateboard_test/joint3_effort_controller/command', Float64, queue_size=10)
        self.pub4 = rospy.Publisher('/skateboard_test/joint4_effort_controller/command', Float64, queue_size=10)

    def move(self, key):
        torque = Float64()
        torque.data = 1

        neg_torque = Float64()
        neg_torque.data = -1

        if key == pygame.K_w:
            self.publish_torque(neg_torque, neg_torque, neg_torque, neg_torque)
        # elif key == pygame.K_a:
        #     self.publish_torque(torque, torque, neg_torque, neg_torque)
        elif key == pygame.K_s:
            self.publish_torque(torque, torque, torque, torque)
        # elif key == pygame.K_d:
        #     self.publish_torque(neg_torque, neg_torque, torque, torque)
        else:
            self.publish_torque(Float64(), Float64(), Float64(), Float64())

    def publish_torque(self, t1, t2, t3, t4):
        self.pub1.publish(t1)
        self.pub2.publish(t2)
        self.pub3.publish(t3)
        self.pub4.publish(t4)

def image_callback(msg):
    image = cam.get_image(msg)
    cam.show_image(image)

    if cv2.waitKey(1) % 256 == 32:
        print("Image Captured and Saved")
        cam.save_image(image)

def main():
    global cam, robot

    cam = Camera()
    robot = Robot()

    rospy.init_node("image_node", anonymous=True)

    sub = rospy.Subscriber('/camera/color/image_raw', Image, image_callback, queue_size=10)
    rate = rospy.Rate(10)

    pygame.init()
    pygame.display.set_mode((1, 1))

    print("Press 'W' to move forward, 'A' to turn left, 'S' to move backward, 'D' to turn right, and 'Q' to quit.")

    while not rospy.is_shutdown():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    robot.move(event.key)
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        rate.sleep()

if __name__ == '__main__':
    try:
        main()

    except rospy.ROSInterruptException:
        pass
    except SystemExit:
        pass

