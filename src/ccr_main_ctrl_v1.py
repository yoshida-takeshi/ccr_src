#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
import rospy
import numpy as np
from time import sleep

sys.path.append("/home/ubuntu/ros_groupE_ws/src/crane_plus_src/src/")
import write_char_v4 as write_char
import write_char_v3 as write_char3
import jtalk_v1 as jtalk
import ccr_ctrl_v1 as ccr_ctrl


class ccr_main_ctrl:
    ########################################
    #INIT
    def __init__(self,args):
        ARM_ON=False
        GRAPH_ON=True
        CmdFile = args[1]

        self.wc=write_char.write_char(ARM_ON,GRAPH_ON)
        self.wc3=write_char3.write_char(ARM_ON,GRAPH_ON) #zantei
        self.jt=jtalk.jtalk()
        self.cc=ccr_ctrl.ccr_ctrl()

        self.setup_param()
        self.main_loop(CmdFile)


    ########################################
    #パラメータ初期設定
    def setup_param(self):
        self.wc.HeightDown=0.093
        self.wc.FontSize=0.05
        self.wc.Rotate=0
        self.y=self.wc.y_Bottom+0.09
        self.x=-self.wc.FontSize/2

        #zantei
        self.wc3.HeightDown=0.093
        self.wc3.FontSize=0.05
        self.wc3.Rotate=0

    ########################################
    #メイン処理
    def main_loop(self,CmdFile):
        f = open(CmdFile)
        CmdLineAll = f.readlines()
        f.close()

        for CmdLine in CmdLineAll:
            CmdLine=CmdLine.rstrip()
            CmdWord=CmdLine.split()

            if len(CmdWord)==0: continue
            if re.search("^#",CmdLine): continue
            print("CMD:"+CmdLine)
                
            if CmdWord[0]=="write":
                self.cmd_write(CmdWord)
            elif CmdWord[0]=="fontsize":
                self.cmd_fontsize(CmdWord)
            elif CmdWord[0]=="locate":
                self.cmd_locate(CmdWord)
            elif CmdWord[0]=="speak":
                self.cmd_speak(CmdWord)
            elif CmdWord[0]=="speak_file":
                self.cmd_speak_file(CmdWord)
            elif CmdWord[0]=="wait":
                self.cmd_wait(CmdWord)
            elif CmdWord[0]=="ccr_move":
                self.cmd_ccr_move(CmdWord)
            elif CmdWord[0]=="ccr_left":
                self.cmd_ccr_left(CmdWord)
            elif CmdWord[0]=="ccr_right":
                self.cmd_ccr_right(CmdWord)
            elif CmdWord[0]=="write3": #zantei
                self.cmd_write3(CmdWord)
            elif CmdWord[0]=="fontsize3": #zantei
                self.cmd_fontsize3(CmdWord)
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
    #CMD:CCR_MOVE
    def cmd_ccr_move(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_move <distance>)")
            return
        self.cc.ccr_move(float(CmdWord[1]),0)

    ########################################
    #CMD:CCR_LEFT
    def cmd_ccr_left(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_left <distance>)")
            return
        self.cc.ccr_move(0,float(CmdWord[1]))

    ########################################
    #CMD:CCR_ROGHT
    def cmd_ccr_right(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: ccr_right <distance>)")
            return
        self.cc.ccr_move(0,-float(CmdWord[1]))


    ########################################
    #zantei CMD:文字を書く
    def cmd_write3(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: write <font_file>)")
            return
        fontfile=CmdWord[1]
        data = np.load(fontfile)
        self.wc3.write_char(data,self.x,self.y)
        

    ########################################
    #zantei CMD:FONTSIZE変更
    def cmd_fontsize3(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: fontsize <font_size[m]>)")
            return
        self.wc3.FontSize=float(CmdWord[1])

        

if __name__ == '__main__':
    try:
        args = sys.argv
        if len(args)==2:
            ts = ccr_main_ctrl(args)
            rospy.spin()
        else:
            print("usage: %s <command_file>" % args[0])

    except rospy.ROSInterruptException: pass
