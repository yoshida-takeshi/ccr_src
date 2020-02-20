import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#cv2.namedWindow("frame")
#cv2.namedWindow("mask")
#cv2.namedWindow("res")

def adjust(img, alpha=1.0, beta=0.0):
    dst=alpha*img+beta
    return np.clip(dst,0,255).astype(np.uint8)

while(1):

    # Take each frame
    _, frame = cap.read()
    #frame=adjust(frame,alpha=2.0, beta=0.0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    #pink
    #lower_blue = np.array([150,75,75])
    #upper_blue = np.array([180,255,255])

    #aka
    #lower_blue = np.array([150,50,30])
    #upper_blue = np.array([180,255,255])
    #lower_blue = np.array([0,75,75])
    #upper_blue = np.array([10,255,255])

    #kiro
    #lower_blue = np.array([10,75,75])
    #upper_blue = np.array([40,255,255])

    #midori
    #lower_blue = np.array([70,70,70])
    #upper_blue = np.array([100,255,255])

    #ao
    lower_blue = np.array([110,75,75])
    upper_blue = np.array([140,255,255])

    #black
    #lower_blue = np.array([0  ,50  ,0])
    #upper_blue = np.array([255,255,10])
    #white
    #lower_blue = np.array([0  ,0  ,50])
    #upper_blue = np.array([255,10,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
