#!/usr/bin/env python
#coding: utf-8

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Byte
from ccr_msgs.msg import Drive
from ccr_msgs.msg import LEDBoardEvent

#import sys
#import subprocess
#from datetime import datetime

class ccr_ctrl:
    ########################################    
    #INIT
    def __init__(self):
        try:
            rospy.init_node('ccr_ctrl', anonymous=True)
        except rospy.exceptions.ROSException:
            print("Information: skip init_node")
        self.mode_pub = rospy.Publisher('/mobile_base/command/mode', String, queue_size=1000)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1000)
        rospy.Subscriber('/mobile_base/event/mode',Byte, self.modeCallback)
        rospy.Subscriber('/mobile_base/event/led_board',LEDBoardEvent, self.led_boardCallback)

        r = rospy.Rate(1)
        self.mode=0
        self.drive=Drive()
        self.led_board=LEDBoardEvent()

        self.normal_mode()


    ########################################    
    #ccr_move
    def ccr_move(self,vel,rad):
        twist=Twist()
        r = rospy.Rate(1)

        twist.linear.x=vel
        twist.angular.z=rad
        r.sleep()
        self.twist_pub.publish(twist)
        r.sleep()
        
    ########################################    
    #wait_button
    def wait_button(self,code):
        r = rospy.Rate(1)
        while(1):
            r.sleep()
            if (self.led_board&code) :
                break


    ########################################    
    #return normal mode
    def normal_mode(self):
        r = rospy.Rate(1)
        self.mode=3
        while (self.mode==3):
            r.sleep()
            self.mode_pub.publish("normal")
            r.sleep()


    ########################################    
    #get mode
    def modeCallback(self, mode):
        self.mode=mode.data

    ########################################    
    #get led_board
    def led_boardCallback(self, led_board):
        self.led_board=led_board.event


if __name__ == '__main__':
    try:
        ts = ccr_ctrl()
        rospy.spin()
    except rospy.ROSInterruptException: pass

