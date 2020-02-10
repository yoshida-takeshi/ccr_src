#!/usr/bin/env python
#coding: utf-8

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Byte
from ccr_msgs.msg import Drive
from ccr_msgs.msg import LEDBoardEvent
from ccr_msgs.msg import LEDBoardCommand

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
        self.led_pub   = rospy.Publisher('/mobile_base/command/ledboard_Command', LEDBoardCommand, queue_size=1000)

        rospy.Subscriber('/mobile_base/event/mode',Byte, self.modeCallback)
        rospy.Subscriber('/mobile_base/event/led_board',LEDBoardEvent, self.led_boardCallback)

        rospy.Timer(rospy.Duration(0.1), self.timerCallback)

        r = rospy.Rate(10)
        self.mode=0
        self.drive=Drive()
        self.led_cmd=LEDBoardCommand()
        self.led_board=LEDBoardEvent()

        self.normal_mode()
        #self.manual_mode()


    ########################################
    #ccr_move
    def ccr_move(self,vel,rad):
        twist=Twist()
        r = rospy.Rate(10)
        step=3

        twist.linear.x=vel/step
        twist.angular.z=rad/step
        self.normal_mode()
        for t in range(10):
            r.sleep()
        for i in range(step):
            self.twist_pub.publish(twist)
            for t in range(10):
                r.sleep()
        

    ########################################
    #wait_button
    def wait_button(self,code):
        r = rospy.Rate(10)
        self.led_board=0
        self.led_cmd.cmd2=1 #LED ON
        while(1):
            r.sleep()
            if (self.led_board&code) :
                break
        self.led_cmd.cmd2=0 #LED OFF


    ########################################
    #change to normal_mode
    def normal_mode(self):
        r = rospy.Rate(10)
        if (self.mode!=1):
            print("wait to normal mode.")
            while (self.mode!=1):
                r.sleep()
                self.mode_pub.publish("normal")
                r.sleep()
            print("=> normal mode.")

    ########################################
    #change to manual_mode
    def manual_mode(self):
        r = rospy.Rate(10)
        if (self.mode!=2):
            print("wait to manual mode.")
            while (self.mode!=2):
                r.sleep()
                self.mode_pub.publish("manual")
                r.sleep()
            print("=> manual mode.")


    ########################################
    #get mode
    def modeCallback(self, mode):
        self.mode=mode.data
        #LED Indicator
        if(self.mode==1): self.led_cmd.cmd3=1 #Normal=>ON
        if(self.mode==2): self.led_cmd.cmd3=2 #Manual=>FLASH_SLOW
        if(self.mode==3): self.led_cmd.cmd3=3 #Error=> FLASH_FAST

    ########################################
    #get led_board
    def led_boardCallback(self, led_board):
        self.led_board=led_board.event
        if self.led_board&32: #"mainichi" -> normal_mode
            self.normal_mode()
        if self.led_board&16: #"yoyaku" -> manual_mode
            self.manual_mode()

    ########################################
    #set LED
    def set_led(self):
        r = rospy.Rate(10)
        r.sleep()
        self.led_pub.publish(self.led_cmd)
        r.sleep()
        self.led_pub.publish(self.led_cmd)
        r.sleep()

    ########################################
    #set 7seg
    def set_7seg(self,n):
        if(0<=n<=31):
            self.led_cmd.cmd1=32+n
        else:
            self.led_cmd.cmd1=0


    ########################################
    #Timer
    def timerCallback(self, event):
        self.set_led()




if __name__ == '__main__':
    try:
        ts = ccr_ctrl()
        rospy.spin()
    except rospy.ROSInterruptException: pass

