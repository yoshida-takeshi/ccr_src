#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import rospy
import cv2
import numpy as np
#import subprocess
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class cam_Ctrl:

    def __init__(self):
        try:
            rospy.init_node('control_rulo', anonymous=True)
        except rospy.exceptions.ROSException:
            print("Information: skip init_node")

        self.twist_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1000)
        #カメラ画像を取得するたびcallback関数を呼び出す
        #self._image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.imageCallback)
        #self._bridge = CvBridge()
 
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.twist_pub.publish(twist)

        #self.move_color("back","blue")
	
    def move_color(self,direct,color):	
	
        if color == "blue":
            # ここでは青色を抽出するので120±20を閾値とした
            LOW_COLOR = np.array([100, 75, 75])
            HIGH_COLOR = np.array([140, 255, 255])
        elif color == "red":
            # ここでは青色を抽出するので120±20を閾値とした
            LOW_COLOR = np.array([100, 75, 75])
            HIGH_COLOR = np.array([140, 255, 255])
        elif color == "green":
            # ここでは青色を抽出するので120±20を閾値とした
            LOW_COLOR = np.array([40, 75, 75])
            HIGH_COLOR = np.array([80, 255, 255])
        elif color == "yellow":
            # ここでは青色を抽出するので120±20を閾値とした
            LOW_COLOR = np.array([72, 75, 75])
            HIGH_COLOR = np.array([112, 255, 255])
        elif color == "black":
            # ここでは青色を抽出するので120±20を閾値とした
            LOW_COLOR = np.array([0, 0, 0])
            HIGH_COLOR = np.array([20, 20, 20])
        elif color == "white":
            # ここでは青色を抽出するので120±20を閾値とした
            LOW_COLOR = np.array([0, 0, 200])
            HIGH_COLOR = np.array([20, 20, 255])
        else:
            # ここでは青色を抽出するので120±20を閾値とした
            LOW_COLOR = np.array([100, 75, 75])
            HIGH_COLOR = np.array([140, 255, 255])
            

    	# 抽出する青色の塊のしきい値
        AREA_RATIO_THRESHOLD = 0.005
        # webカメラを扱うオブジェクトを取得
        cap = cv2.VideoCapture(0)

        r=rospy.Rate(10)

        while True:
            ret,frame = cap.read()
            #r = rospy.Rate(20)

            if ret is False:
                print("cannot read image")
                continue
		
            #画像サイズ
            h,w,c = frame.shape
        	#停止位置
            stop_line = h/2
        	#停止位置マージン
            stop_margin = 20

        	# 位置を抽出
            pos = self.find_specific_color(
                    frame,
                    AREA_RATIO_THRESHOLD,
                    LOW_COLOR,
                    HIGH_COLOR
                    )

            if pos is not None:
                # 抽出した座標に丸を描く
                cv2.circle(frame,pos,10,(0,0,255),-1)


                if (stop_line + stop_margin) < pos[1] :
                    twist = Twist()
                    twist.linear.x = -0.02
                    self.twist_pub.publish(twist)
                elif pos[1] < (stop_line - stop_margin):
                    twist = Twist()
                    twist.linear.x = 0.02
                    self.twist_pub.publish(twist)
                else:
                    twist = Twist()
                    twist.linear.x = 0
                    for i in range(100):
                    	self.twist_pub.publish(twist)

                    print("finish")			
                    break
            else:
                twist = Twist()
                if direct == "forward":
                    twist.linear.x = 0.10
                elif direct == "back":
                    twist.linear.x = -0.10
                else:
                    twist.linear.x = 0.10
                self.twist_pub.publish(twist)

            #r.sleep()
            # 画面に表示する
            #cv2.imshow('frame',frame)

        cv2.destroyAllWindows()
    
    def find_specific_color(self,frame,AREA_RATIO_THRESHOLD,LOW_COLOR,HIGH_COLOR):
        
        #高さ、幅、チャネル数
        h,w,c = frame.shape
        #hsv色空間に変換
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #色を抽出
        ex_image = cv2.inRange(hsv,LOW_COLOR,HIGH_COLOR)
        #輪郭抽出
        _,contours,hierarchy = cv2.findContours(ex_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #面積を計算
        areas = np.array(list(map(cv2.contourArea,contours)))
        if len(areas) == 0 or np.max(areas) / (h*w) < AREA_RATIO_THRESHOLD:
            # 見つからなかったらNoneを返す
            print("the area is too small")
            return None
        else:
            # 面積が最大の塊の重心を計算し返す
            max_idx = np.argmax(areas)
            max_area = areas[max_idx]
            result = cv2.moments(contours[max_idx])
            x = int(result["m10"]/result["m00"])
            y = int(result["m01"]/result["m00"])
            return (x,y)

 
if __name__ == '__main__':
 
    try:
        ts = cam_Ctrl()
        rospy.spin()
    except rospy.ROSInterruptException: pass
