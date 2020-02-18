#! /usr/bin/env python
# -*- coding: utf-8 -*-

CCR_ON=True

import sys
import re
import rospy
import numpy as np
from time import sleep

sys.path.append("/home/ubuntu/ros_groupE_ws/src/crane_plus_src/src/")
import write_char_v6 as write_char
import jtalk_v1 as jtalk
import cam_rulo_v3 as cam_Ctrl
try:
    import ccr_ctrl_v1 as ccr_ctrl
except:
    CCR_ON=False


class ccr_main_ctrl:
    ########################################
    #INIT
    def __init__(self,args):
        ARM_ON=True
        GRAPH_ON=True
        CmdFile = args[1]

        try:
            rospy.init_node('ccr_main_ctrl', anonymous=True)
        except rospy.exceptions.ROSException:
            print("Information: skip init_node")

        self.wc=write_char.write_char(ARM_ON,GRAPH_ON)
        if CCR_ON==True:
            self.cc=ccr_ctrl.ccr_ctrl()
        self.jt=jtalk.jtalk()
        self.ct=cam_Ctrl.cam_Ctrl()

        self.setup_param()
        self.main_loop(CmdFile)


    ########################################
    #パラメータ初期設定
    def setup_param(self):
        #self.wc.HeightDown=0.093
        #self.wc.FontSize=0.05
        self.wc.Rotate=0
        #self.y=self.wc.y_Bottom+0.09
        #self.x=-self.wc.FontSize/2
        self.y=self.wc.y_Bottom+0.21
        self.x=-self.wc.FontSize/2

    ########################################
    #メイン処理
    def main_loop(self,CmdFile):
        f = open(CmdFile)
        CmdLineAll = f.readlines()
        f.close()

        print(len(CmdLineAll))
        #for CmdLine in CmdLineAll:
        self.pc=0
        while(self.pc<len(CmdLineAll)):
            CmdLine=CmdLineAll[self.pc]
            CmdLine=CmdLine.rstrip()
            CmdWord=CmdLine.split()

            self.pc+=1
            if len(CmdWord)==0: continue
            if re.search("^#",CmdLine): continue
            print("CMD:"+CmdLine)
                
            if CmdWord[0]=="write":
                self.cmd_write(CmdWord)
            elif CmdWord[0]=="fontsize":
                self.cmd_fontsize(CmdWord)
            elif CmdWord[0]=="locate":
                self.cmd_locate(CmdWord)
            elif CmdWord[0]=="refill":
                self.cmd_refill(CmdWord)
            elif CmdWord[0]=="clear":
                self.cmd_clear(CmdWord)
            elif CmdWord[0]=="speak":
                self.cmd_speak(CmdWord)
            elif CmdWord[0]=="speak_file":
                self.cmd_speak_file(CmdWord)
            elif CmdWord[0]=="wait":
                self.cmd_wait(CmdWord)
            elif CmdWord[0]=="wait_enter":
                self.cmd_wait_enter(CmdWord)
            elif CmdWord[0]=="ccr_move":
                self.cmd_ccr_move(CmdWord)
            elif CmdWord[0]=="ccr_move_line":
                self.cmd_ccr_move_line(CmdWord)
            elif CmdWord[0]=="ccr_left":
                self.cmd_ccr_left(CmdWord)
            elif CmdWord[0]=="ccr_right":
                self.cmd_ccr_right(CmdWord)
            elif CmdWord[0]=="ccr_button":
                self.cmd_ccr_button(CmdWord)
            elif CmdWord[0]=="ccr_7seg":
                self.cmd_ccr_7seg(CmdWord)
            elif CmdWord[0]=="goto":
                self.cmd_goto(CmdWord)
            else:
                print("Error: Unknown command => %s" % CmdLine)
            
        key = raw_input('Please enter to finish.')
        exit()


    ########################################
    #CMD:文字を書く
    def cmd_write(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: write <font_file>)")
            return
        fontfile=CmdWord[1]
        data = np.load(fontfile)
        self.wc.write_char(data,self.x,self.y)
        

    ########################################
    #CMD:FONTSIZE変更
    def cmd_fontsize(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: fontsize <font_size[m]>)")
            return
        self.wc.FontSize=float(CmdWord[1])

    ########################################
    #CMD:墨補充
    def cmd_refill(self,CmdWord):
        if len(CmdWord)!=3:
            print("Error: Invalid args (usage: refill <x[m]> <y[m]>)")
            return
        self.wc.refill(float(CmdWord[1]),float(CmdWord[2]))

    ########################################
    #CMD:GRAPH CLEAR
    def cmd_clear(self,CmdWord):
        if len(CmdWord)!=1:
            print("Error: Invalid args (usage: clear)")
            return
        self.wc.graph_clear()


    ########################################
    #CMD:文字座標変更
    def cmd_locate(self,CmdWord):
        if len(CmdWord)!=3:
            print("Error: Invalid args (usage: locate <x[m]> <y[m])")
            return
        self.x=float(CmdWord[1])
        self.y=float(CmdWord[2])


    ########################################
    #CMD:しゃべる
    def cmd_speak(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: speak <text>)")
            return
        self.jt.jtalk(CmdWord[1])


    ########################################
    #CMD:しゃべる(TEXTFILE読込)
    def cmd_speak_file(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: speak_file <text_file>)")
            return
        self.jt.jtalk_by_file(CmdWord[1])

    ########################################
    #CMD:WAIT
    def cmd_wait(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: wait <second>)")
            return
        sleep(int(CmdWord[1]))

    ########################################
    #CMD:WAIT_ENTER
    def cmd_wait_enter(self,CmdWord):
        if len(CmdWord)!=1:
            print("Error: Invalid args (usage: wait_enter)")
            return
        key = raw_input('Please enter.')

    ########################################
    #CMD:CCR_MOVE
    def cmd_ccr_move(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_move <distance>)")
            return
        self.cc.ccr_move(float(CmdWord[1]),0)

    ########################################
    #CMD:CCR_MOVE_LINE
    def cmd_ccr_move_line(self,CmdWord):
        if len(CmdWord)!=3:
            print("Error: Invalid args (usage: ccr_move_line <distance>)")
            return
        self.ct.move_color(CmdWord[1],CmdWord[2])

    ########################################
    #CMD:CCR_LEFT
    def cmd_ccr_left(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_left <distance>)")
            return
        self.cc.ccr_move(0,float(CmdWord[1]))

    ########################################
    #CMD:CCR_RIGHT
    def cmd_ccr_right(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_right <distance>)")
            return
        self.cc.ccr_move(0,-float(CmdWord[1]))

    ########################################
    #CMD:CCR_BUTTON
    def cmd_ccr_button(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_button <code>)")
            return
        self.cc.wait_button(int(CmdWord[1]))

    ########################################
    #CMD:CCR_7SEG
    def cmd_ccr_7seg(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_7seg <n>)")
            return
        self.cc.set_7seg(int(CmdWord[1]))


    ########################################
    #CMD:GOTO
    def cmd_goto(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: goto <line_number>)")
            return
        self.pc=int(CmdWord[1])


if __name__ == '__main__':
    try:
        args = sys.argv
        if len(args)==2:
            ts = ccr_main_ctrl(args)
            rospy.spin()
        else:
            print("usage: %s <command_file>" % args[0])

    except rospy.ROSInterruptException: pass
