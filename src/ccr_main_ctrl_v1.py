#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
import rospy
import numpy as np
from time import sleep

sys.path.append("/home/ubuntu/ros_groupE_ws/src/crane_plus_src/src/")
import write_char_v2 as write_char
import jtalk_v1 as jtalk


class ccr_main_ctrl:
    ########################################
    #INIT
    def __init__(self,args):
        ARM_ON=False
        GRAPH_ON=True
        CmdFile = args[1]

        self.wc=write_char.write_char(ARM_ON,GRAPH_ON)
        self.jt=jtalk.jtalk()
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


        

if __name__ == '__main__':
    try:
        args = sys.argv
        if len(args)==2:
            ts = ccr_main_ctrl(args)
            rospy.spin()
        else:
            print("usage: %s <command_file>" % args[0])

    except rospy.ROSInterruptException: pass
