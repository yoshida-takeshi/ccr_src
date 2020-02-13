# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:14:39 2020

@author: 4035395
"""

import numpy as np
import cv2

b, g, r = map(int, input().split())
rgb_color = np.uint8([[[r, g, b]]])  # here insert the bgr values which you want to convert to hsv
hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_BGR2HSV)
print("HSV value:",hsv_color)
lowerLimit = hsv_color[0][0][0] - 20, 100, 100
upperLimit = hsv_color[0][0][0] + 20, 255, 255
print("Upper_limit:",upperLimit)
print("Lower_limit;",lowerLimit)
