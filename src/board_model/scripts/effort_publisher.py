#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float64

def main():
    
    rospy.init_node("effort_node",anonymous =True)
    
    j1 = rospy.Publisher('/skateboard_test/joint1_effort_controller/command', Float64, queue_size=10)
    j2 = rospy.Publisher('/skateboard_test/joint2_effort_controller/command', Float64, queue_size=10)
    j3 = rospy.Publisher('/skateboard_test/joint3_effort_controller/command', Float64, queue_size=10)
    j4 = rospy.Publisher('/skateboard_test/joint4_effort_controller/command', Float64, queue_size=10)
    
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown:
        torque = 100.0
        j1.publish(torque)
        j2.publish(torque)
        j3.publish(torque)
        j4.publish(torque)
        rospy.loginfo("Publishing Torque...")
        rate.sleep()
        
if __name__ == '__main__':
    try:
        main()
            
    except rospy.ROSInterruptException:
        pass
    
    
