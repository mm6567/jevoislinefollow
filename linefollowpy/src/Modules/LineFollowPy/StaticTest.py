#!python3.5
# static testing for line following
import numpy as np
import cv2

img = cv2.imread('../../../linepic1.jpg')

cv2.imshow('raw color',img)

height, width, chans = img.shape


cv2.waitKey(0)
cv2.destroyAllWindows()
