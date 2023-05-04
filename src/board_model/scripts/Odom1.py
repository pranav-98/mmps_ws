#! /usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry

import tf_conversions

import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import Float64
def handle_vehicle_pose(msg):

    x = msg.pose[1].position.x 
    y = msg.pose[1].position.y
    dx = msg.twist[1].linear.x
    dy = msg.twist[1].linear.y



    pos = Float64()
    vel = Float64()

    pos.data = x
    vel.data = dx

    position_publisher.publish(pos)
    velocty_publisher.publish(vel)
    




    
if __name__ == '__main__':
    rospy.init_node('tf_odom_publisher')
    rospy.Subscriber('/gazebo/model_states', ModelStates, handle_vehicle_pose)
    position_publisher = rospy.Publisher('/position', Float64, queue_size=1)
    velocty_publisher = rospy.Publisher('/velocity', Float64, queue_size=1)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
