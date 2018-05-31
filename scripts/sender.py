#!/usr/bin/env python
__author__ = 'flier'
import rospy
import tf
import leap_interface
#from leap_motion.msg import leap
from leap_motion.msg import leapros
from geometry_msgs.msg import PoseStamped

# Obviously, this method publishes the data defined in leapros.msg to /leapmotion/data
def sender():
    li = leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    # pub     = rospy.Publisher('leapmotion/raw',leap)
    #pub_ros   = rospy.Publisher('leapmotion/data',leapros,queue_size=2)
    pub_leap_pos   = rospy.Publisher('/left_controller_as_posestamped', PoseStamped,queue_size=2)
    rospy.init_node('leap_pub')

    while not rospy.is_shutdown():
        # hand_direction_   = li.get_hand_direction()
        # hand_normal_      = li.get_hand_normal()
        hand_palm_pos_    = li.get_hand_palmpos()
        hand_pitch_       = li.get_hand_pitch()
        hand_roll_        = li.get_hand_roll()
        hand_yaw_         = li.get_hand_yaw()
        msg = leapros()
        # msg.direction.x = hand_direction_[0]
        # msg.direction.y = hand_direction_[1]
        # msg.direction.z = hand_direction_[2]
        # msg.normal.x = hand_normal_[0]
        # msg.normal.y = hand_normal_[1]
        # msg.normal.z = hand_normal_[2]
        msg.palmpos.x = hand_palm_pos_[0]
        msg.palmpos.y = hand_palm_pos_[1]
        msg.palmpos.z = hand_palm_pos_[2]
        msg.ypr.x = hand_yaw_
        msg.ypr.y = hand_pitch_
        msg.ypr.z = hand_roll_


        ps = PoseStamped()
        ps.header.frame_id = "map"
        ps.header.stamp = rospy.Time.now()
        ps.pose.position.x = -msg.palmpos.z/1000
        ps.pose.position.y = -msg.palmpos.x/1000
        ps.pose.position.z =  msg.palmpos.y/1000
        
        quaternion = tf.transformations.quaternion_from_euler(-msg.ypr.z, -msg.ypr.x, msg.ypr.y)
        ps.pose.orientation.x = quaternion[0]
        ps.pose.orientation.y = quaternion[1]
        ps.pose.orientation.z = quaternion[2]
        ps.pose.orientation.w = quaternion[3]


        pub_leap_pos.publish(ps)
        # Save some CPU time, circa 100Hz publishing.
        rospy.sleep(0.01)


if __name__ == '__main__':
    try:
        sender()
    except rospy.ROSInterruptException:
        pass
