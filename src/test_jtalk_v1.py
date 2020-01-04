#!/usr/bin/env python
#coding: utf-8
import sys
import subprocess
from datetime import datetime

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    #htsvoice=['-m','/usr/share/hts-voice/mei/mei_angry.htsvoice']
    #htsvoice=['-m','/usr/share/hts-voice/mei/mei_bashful.htsvoice']
    #htsvoice=['-m','/usr/share/hts-voice/mei/mei_happy.htsvoice']
    #htsvoice=['-m','/usr/share/hts-voice/mei/mei_sad.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)

    #for Python2
    c.stdin.write(t)
    #for Python3
    #c.stdin.write(t.encode())

    c.stdin.close()
    c.wait()

    print(t)
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)

def say_datetime():
    d = datetime.now()
    text = ""
    text += '%s月%s日、%s時%s分%s秒。' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)

def say_text(infile):
    f = open(infile)
    lines2 = f.readlines()
    f.close()
    text=""
    for line in lines2:
        #print(line)
        text+=line.rstrip()+" "
    jtalk(text)

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        say_datetime()
    else:
        say_text(args[1])

