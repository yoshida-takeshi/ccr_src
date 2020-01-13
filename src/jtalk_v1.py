#!/usr/bin/env python
#coding: utf-8
import sys
import subprocess
from datetime import datetime

class jtalk:
    ########################################    
    #INIT
    def __init__(self):
        self.tmpwave='/tmp/open_jtalk.wav'
        open_jtalk=['open_jtalk']
        mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
        htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
        #htsvoice=['-m','/usr/share/hts-voice/mei/mei_angry.htsvoice']
        #htsvoice=['-m','/usr/share/hts-voice/mei/mei_bashful.htsvoice']
        #htsvoice=['-m','/usr/share/hts-voice/mei/mei_happy.htsvoice']
        #htsvoice=['-m','/usr/share/hts-voice/mei/mei_sad.htsvoice']
        speed=['-r','1.0']
        outwav=['-ow',self.tmpwave]
        self.cmd=open_jtalk+mech+htsvoice+speed+outwav

    ########################################    
    #jtalk
    def jtalk(self,t):
        c = subprocess.Popen(self.cmd,stdin=subprocess.PIPE)

        #for Python2
        c.stdin.write(t)
        #for Python3
        #c.stdin.write(t.encode())

        c.stdin.close()
        c.wait()

        print("jtalk: %s" % t)
        aplay = ['aplay','-q',self.tmpwave]
        wr = subprocess.Popen(aplay)
        wr.wait()

    def jtalk_by_file(self,infile):
        f = open(infile)
        lines2 = f.readlines()
        f.close()
        text=""
        for line in lines2:
            text+=line.rstrip()+" "
        self.jtalk(text)

if __name__ == '__main__':
    try:
        ts = jtalk()
        rospy.spin()
    except rospy.ROSInterruptException: pass

