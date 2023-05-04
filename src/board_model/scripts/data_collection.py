#!/usr/bin/env python3
import rospy
import cv2
import os
import numpy as np
from sensor_msgs.msg import Image, PointCloud2
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float64
import message_filters
import sensor_msgs.point_cloud2 as pc2


class Camera(object):

    def __init__(self):

        # ROS To OpenCV Converter.
        self.bridge = CvBridge()
        self.counter = 0

    def get_image(self, msg, encoding):
        self.image = self.bridge.imgmsg_to_cv2(msg, encoding)
        return self.image

    @staticmethod
    def show_image(window_name, image):
        cv2.imshow(window_name, image)
        cv2.waitKey(1)

    def save_image(self, image_rgb, image_depth):
        self.counter += 1
        
        rgb_path = "/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/RGB_images"
        if not os.path.exists(rgb_path): # Create the directory if it doesn't exist
            os.makedirs(rgb_path)
        cv2.imwrite("/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/RGB_images/img" + str(self.counter) + ".jpg", image_rgb)

        depth_path = "/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/depth_images"
        if not os.path.exists(depth_path): # Create the directory if it doesn't exist
            os.makedirs(depth_path)
        cv2.imwrite("/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/depth_images/img" + str(self.counter) + ".jpg", image_depth)
        # normalized_depth_image = cv2.normalize(image_depth, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        # cv2.imwrite("/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/depth_images/img" + str(self.counter) + ".jpg", normalized_depth_image)

    def save_point_cloud_to_ply(self, point_cloud):
        # Create the directory if it doesn't exist
        path = "/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/PointClouds"
        if not os.path.exists(path):
            os.makedirs(path)

        # Combine the directory path with the filename
        file_path = os.path.join(path, "pc"+str(self.counter)+".ply")

        with open(file_path, 'w') as ply_file:
            ply_file.write("ply\n")
            ply_file.write("format ascii 1.0\n")
            ply_file.write("element vertex {}\n".format(point_cloud.shape[0]))
            ply_file.write("property float x\n")
            ply_file.write("property float y\n")
            ply_file.write("property float z\n")
            ply_file.write("end_header\n")

            for point in point_cloud:
                ply_file.write("{} {} {}\n".format(point[0], point[1], point[2]))


def callback(msg_rgb, msg_depth, msg_point):

    image_rgb = cam.get_image(msg_rgb, "bgr8")
    cam.show_image('RGB Image', image_rgb)

    image_depth = cam.get_image(msg_depth, "passthrough")
    cam.show_image('Depth Image', image_depth)

    # print(image_depth.shape)
    # print(np.nanmax(image_depth))
    # print(np.nanmin(image_depth))

    # Find the locations of NaN values in the image
    # nan_locs = np.isnan(image_depth)

    # Find the locations of positive and negative infinity values in the image
    # pos_inf_locs = np.isposinf(image_depth)
    # neg_inf_locs = np.isneginf(image_depth)

    # if np.any(pos_inf_locs):
    #     print("There are true values in the pos matrix.")
    # else:
    #     print("There are no true values in the pos matrix.")

    # if np.any(neg_inf_locs):
    #     print("There are true values in the neg matrix.")
    # else:
    #     print("There are no true values in the neg matrix.")

    # # Check if any NaN values are closer to the camera than positive infinity values
    # if np.any(nan_locs[:int(nan_locs.shape[0]/2)] & pos_inf_locs[:int(pos_inf_locs.shape[0]/2)]):
    #     print("Near NaN values detected.")

    # # Check if any NaN values are farther from the camera than negative infinity values
    # if np.any(nan_locs[int(nan_locs.shape[0]/2):] & neg_inf_locs[int(neg_inf_locs.shape[0]/2):]):
    #     print("Far NaN values detected.")

    pc_list = list(pc2.read_points(msg_point, field_names=("x", "y", "z"), skip_nans=True)) # Extract x, y, z coordinates from the point_cloud data
    pc_np = np.array(pc_list, dtype=np.float32) # Convert the list of points to a NumPy array

    # if cv2.waitKey(0) % 256 == 32:
    # print("RGB and Depth Images Captured and Saved. Point Cloud saved.")
    # cam.save_image(image_rgb,image_depth)
    # cam.save_point_cloud_to_ply(pc_np) # Save the point cloud to a PLY file

def main():
    global cam

    cam = Camera()

    rospy.init_node("combined_image_node", anonymous=True)

    sub_rgb = message_filters.Subscriber('/camera/color/image_raw', Image)
    sub_depth = message_filters.Subscriber('/kinect/depth/image_raw', Image)
    sub_point = message_filters.Subscriber('/kinect/depth/points', PointCloud2)

    ts = message_filters.ApproximateTimeSynchronizer([sub_rgb, sub_depth,sub_point], queue_size=10, slop=0.05)
    ts.registerCallback(callback)

    rate = rospy.Rate(2)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()

    except rospy.ROSInterruptException:
        pass