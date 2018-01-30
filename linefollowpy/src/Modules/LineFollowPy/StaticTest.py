#!python3.5
# static testing for line following
import numpy as np
import cv2

img = cv2.imread('../../../linepic1.jpg')
cv2.imshow('img',img)

height, width, chans = img.shape

#imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.imshow('imgray',imgray)

#ret, imthresh = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY_INV) #Get Threshold
#cv2.imshow('imthresh 100',imthresh)

#ret, imthresh = cv2.threshold(imgray,128,255,cv2.THRESH_BINARY_INV) #Get Threshold
#cv2.imshow('imthresh 128',imthresh)

imhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#cv2.imshow('imhsv',imhsv)
lowerBound=np.array([0,0,0])
# note that h and s aren't the 0,0 I though by using the online hsv calc
upperBound=np.array([180,255,40])
immask=cv2.inRange(imhsv,lowerBound,upperBound)
#cv2.imshow('immask', immask)

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

immaskOpen=cv2.morphologyEx(immask,cv2.MORPH_OPEN,kernelOpen)
immaskClose=cv2.morphologyEx(immaskOpen,cv2.MORPH_CLOSE,kernelClose)
cv2.imshow('after morphs', immaskClose)

#maskFinal=maskClose
_, conts, _ = cv2.findContours(immaskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img,conts,-1,(255,0,0),3)

cv2.imshow('img with conts',img)

# contours = cv2.findContours(imthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Get contour
# if contours:
    # print(contours)
    # print(contours.sort(key=cv2.contourArea))
    # MainContour = max(contours, key=cv2.contourArea)

# key press has to be in one of the pic windows, not the shell
cv2.waitKey(0)
cv2.destroyAllWindows()



                
