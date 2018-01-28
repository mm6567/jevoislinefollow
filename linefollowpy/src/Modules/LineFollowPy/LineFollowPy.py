import libjevois as jevois
import cv2
import numpy as np

## Simple test of programming JeVois modules in Python
#
# This module by default simply draws a cricle and a test message onto the grabbed video frames.
#
# Feel free to edit it and try something else.
#
# @author mm6567
# 
# @videomapping YUYV 640 480 15.1 YUYV 640 480 15.1 mm6567 LineFollowPy
# @email itti\@usc.edu
# @address University of Southern California, HNB-07A, 3641 Watt Way, Los Angeles, CA 90089-2520, USA
# @copyright Copyright (C) 2017 by Laurent Itti, iLab and the University of Southern California
# @mainurl http://jevois.org
# @supporturl http://jevois.org/doc
# @otherurl http://iLab.usc.edu
# @license GPL v3
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class LineFollowPy:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # A simple frame counter used to demonstrate sendSerial():
        self.frame = 0
        
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("sample", 100, jevois.LOG_INFO)

        # from VisionRace-master
        #self.image = None
        self.contourCenterX = 0
        self.MainContour = None

    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        jevois.LFATAL("process no usb not implemented")

    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and convert it to OpenCV BGR:
        img = inframe.getCvBGR()

#        # Get image width, height, channels in pixels. Beware that if you change this module to get img as a grayscale
#        # image, then you should change the line below to: "height, width = img.shape" otherwise numpy will throw. See
#        # how it is done in the PythonOpenCv module of jevoisbase:
        height, width, chans = img.shape
#
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()

        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convert to Gray Scale
        #ret, thresh = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY_INV) #Get Threshold
        #ret, thresh = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY) #Get Threshold
        #thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #    cv2.THRESH_BINARY_INV,11,2)
        # threshold function description: https://docs.opencv.org/3.3.1/d7/d4d/tutorial_py_thresholding.html
         
        _, self.contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Get contour
                
        self.prev_MC = self.MainContour
        if self.contours:
            self.MainContour = max(self.contours, key=cv2.contourArea)
        
            self.height, self.width  = img.shape[:2]

            self.middleX = int(self.width/2) #Get X coordinate of the middle point
            self.middleY = int(self.height/2) #Get Y coordinate of the middle point
            
            self.prev_cX = self.contourCenterX
            if self.getContourCenter(self.MainContour) != 0:
                self.contourCenterX = self.getContourCenter(self.MainContour)[0]
                if abs(self.prev_cX-self.contourCenterX) > 5:
                    self.correctMainContour(self.prev_cX)
            else:
                self.contourCenterX = 0
            
            self.dir =  int((self.middleX-self.contourCenterX) * self.getContourExtent(self.MainContour))
            
            # convert the gray back to rbg format so can view what is going on with thresholding
            img = cv2.cvtColor(thresh,cv2.COLOR_GRAY2RGB)

            cv2.drawContours(img,self.MainContour,-1,(0,255,0),3) #Draw Contour GREEN
            cv2.circle(img, (self.contourCenterX, self.middleY), 7, (255,255,255), -1) #Draw dX circle WHITE
            cv2.circle(img, (self.middleX, self.middleY), 3, (0,0,255), -1) #Draw middle circle RED
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,str(self.middleX-self.contourCenterX),(self.contourCenterX+20, self.middleY), font, 1,(200,0,200),2,cv2.LINE_AA)
            cv2.putText(img,"Weight:%.3f"%self.getContourExtent(self.MainContour),(self.contourCenterX+20, self.middleY+35), font, 0.5,(200,0,200),1,cv2.LINE_AA)
        
#
#        # Draw a couple of things into the image:
#        # See http://docs.opencv.org/3.2.0/dc/da5/tutorial_py_drawing_functions.html for tutorial
#        # See http://docs.opencv.org/3.0-beta/modules/imgproc/doc/drawing_functions.html and
#        #     http://docs.opencv.org/3.2.0/d6/d6e/group__imgproc__draw.html for reference manual.
#        cv2.circle(img, (int(width/2), int(height/2)), 100, (255,0,0), 3) 
#
#        cv2.putText(img, "mm6567 - frame {}".format(self.frame), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#                    0.5, (0,0,255), 1, cv2.LINE_AA)
#

        # Write frames/s info from our timer (NOTE: does not account for output conversion time):
        fps = self.timer.stop()
        cv2.putText(img, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    
        # Convert our BGR image to video output format and send to host over USB:
        outframe.sendCvBGR(img)
         
        # Send a string over serial (e.g., to an Arduino). Remember to tell the JeVois Engine to display those messages,
        # as they are turned off by default. For example: 'setpar serout All' in the JeVois console:
        jevois.sendSerial("DONE frame {}".format(self.frame));
        self.frame += 1

    # ###################################################################################################
    ## Parse a serial command forwarded to us by the JeVois Engine, return a string
    # This function is optional and only needed if you want your module to handle custom commands. Delete if not needed.
    def parseSerial(self, str):
        print("parseserial received command [{}]".format(str))
        if str == "hello":
            return self.hello()
        return "ERR: Unsupported command"
    
    # ###################################################################################################
    ## Return a string that describes the custom commands we support, for the JeVois help message
    # This function is optional and only needed if you want your module to handle custom commands. Delete if not needed.
    def supportedCommands(self):
        # use \n seperator if your module supports several commands
        return "hello - print hello using python"

    # ###################################################################################################
    ## Internal method that gets invoked as a custom command
    # This function is optional and only needed if you want your module to handle custom commands. Delete if not needed.
    def hello(self):
        return("Hello from python!")
        
    def getContourCenter(self, contour):
        M = cv2.moments(contour)
        
        if M["m00"] == 0:
            return 0
        
        x = int(M["m10"]/M["m00"])
        y = int(M["m01"]/M["m00"])
        
        return [x,y]
        
    def getContourExtent(self, contour):
        area = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)
        rect_area = w*h
        if rect_area > 0:
            return (float(area)/rect_area)
            
    def Aprox(self, a, b, error):
        if abs(a - b) < error:
            return True
        else:
            return False
            
    def correctMainContour(self, prev_cx):
        if abs(prev_cx-self.contourCenterX) > 5:
            for i in range(len(self.contours)):
                if self.getContourCenter(self.contours[i]) != 0:
                    tmp_cx = self.getContourCenter(self.contours[i])[0]
                    if self.Aprox(tmp_cx, prev_cx, 5) == True:
                        self.MainContour = self.contours[i]
                        if self.getContourCenter(self.MainContour) != 0:
                            self.contourCenterX = self.getContourCenter(self.MainContour)[0]
