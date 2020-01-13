#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import rospy
from geometry_msgs.msg import Twist
#from turtlesim.msg import Pose
from sensor_msgs.msg import LaserScan
 
class turtleSim:
    def __init__(self):
        rospy.init_node('move_turtlesim', anonymous=True)
        #self.twist_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1000)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1000)
        #rospy.Subscriber('turtle1/pose',Pose, self.poseCallback)
        rospy.Subscriber('/mobile_base/event/opt_left',LaserScan, self.optCallbackL)
        rospy.Subscriber('/mobile_base/event/opt_right',LaserScan, self.optCallbackR)
        rospy.Subscriber('/mobile_base/event/us_left',LaserScan, self.lsCallbackL)
        rospy.Subscriber('/mobile_base/event/us_right',LaserScan, self.lsCallbackR)
        rospy.Timer(rospy.Duration(0.1), self.timerCallback)
 
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.twist_pub.publish(twist)
 
    def optCallbackL(self, opt):
        self.optL=opt.ranges[0]*100
    def optCallbackR(self, opt):
        self.optR=opt.ranges[0]*100
    def lsCallbackL(self, opt):
        self.lsL=opt.ranges[0]*100
    def lsCallbackR(self, opt):
        self.lsR=opt.ranges[0]*100
 
    def timerCallback(self, event):
        self.setMoveVector(0.2, 10)
        #self.setMoveVector(-0.2,10)
 
    def setMoveVector(self, linear_x, cnt):
        twist = Twist()
        r = rospy.Rate(10)
 
 
        for i in range(0, cnt):
            if self.optL<10 or self.lsL<20:
                twist.linear.x = 0.0
                twist.angular.z = -1.0
            elif self.optR<10 or self.lsR<20:
                twist.linear.x = 0.0
                twist.angular.z = 1.0
            else:
                twist.linear.x = linear_x
                twist.angular.z = 0.0
            
            self.twist_pub.publish(twist)
            print("%d %d %d %d" % (self.optL,self.optR,self.lsL,self.lsR))
            r.sleep()
 
if __name__ == '__main__':
 
    try:
        ts = turtleSim()
        rospy.spin()
    except rospy.ROSInterruptException: pass
