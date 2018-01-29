#!python3.5
# static testing for line following
import numpy as np
import cv2

img = cv2.imread('../../../linepic1.jpg')
cv2.imshow('img',img)

height, width, chans = img.shape

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('imgray',imgray)

ret, imthresh = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY_INV) #Get Threshold
cv2.imshow('imthresh 100',imthresh)

ret, imthresh = cv2.threshold(imgray,128,255,cv2.THRESH_BINARY_INV) #Get Threshold
cv2.imshow('imthresh 128',imthresh)



contours = cv2.findContours(imthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Get contour
# if contours:
    # print(contours)
    # print(contours.sort(key=cv2.contourArea))
    # MainContour = max(contours, key=cv2.contourArea)

# key press has to be in one of the pic windows, not the shell
cv2.waitKey(0)
cv2.destroyAllWindows()



                
