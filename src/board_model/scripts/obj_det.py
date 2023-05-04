#!/usr/bin/env python3
import os
import rospy
import cv2
import tempfile
import glob
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float64
import message_filters
import subprocess

class Camera(object):

    def __init__(self):

        # ROS To OpenCV Converter.
        self.bridge = CvBridge()
        self.counter = -1

    def get_image(self, msg, encoding):
        self.image = self.bridge.imgmsg_to_cv2(msg, encoding)
        return self.image

    @staticmethod
    def show_image(window_name, image):
        cv2.imshow(window_name, image)
        cv2.waitKey(1)

    def save_image(self, image_rgb, image_depth):
        self.counter += 1
        cv2.imwrite("/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/RGB_images/img" + str(self.counter) + ".jpg", image_rgb)

def callback(msg_rgb, msg_depth):

    image_rgb = cam.get_image(msg_rgb, "bgr8")
    # cam.show_image('RGB Image', image_rgb)

    # image_depth = cam.get_image(msg_depth, "passthrough")
    # cam.show_image('Depth Image', image_depth)

    # Save image_rgb as a temporary file
    temp_image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    cv2.imwrite(temp_image_file.name, image_rgb)
 
    # Pass the temporary file's path as the source
    command = f"python3 detect.py --weights runs/train/exp/weights/best.pt --img 640 --conf 0.4 --source {temp_image_file.name}"
    subprocess.run(command, shell=True, check=True)

    # Remove the temporary file
    temp_image_file.close()
    os.unlink(temp_image_file.name)

    # Define the directory path
    cam.counter += 1
    base_dir = '/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/det_output/yolov5/runs/detect'
    if cam.counter > 0:
        folder_name = f"exp{cam.counter}"
    else:
        folder_name = f"exp"
    image_dir = os.path.join(base_dir, folder_name)

    # Get the list of .jpg image files
    image_file = glob.glob(os.path.join(image_dir, '*.jpg'))
    latest_image_file = max(image_file, key=os.path.getmtime)
    latest_image = cv2.imread(latest_image_file)
    cam.show_image('RGB Image', latest_image)

    # print("RGB and Depth Images Captured and Saved")
    # cam.save_image(image_rgb,image_depth)


def main():
    os.chdir('/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/det_output/yolov5/')
    global cam

    cam = Camera()

    rospy.init_node("obj_det", anonymous=True)

    sub_rgb = message_filters.Subscriber('/camera/color/image_raw', Image)
    sub_depth = message_filters.Subscriber('/kinect/depth/image_raw', Image)

    ts = message_filters.ApproximateTimeSynchronizer([sub_rgb, sub_depth], queue_size=10, slop=0.01)
    ts.registerCallback(callback)

    rate = rospy.Rate(1)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()

    except rospy.ROSInterruptException:
        pass