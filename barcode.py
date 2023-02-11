# import the necessary packages
import numpy as np
import imutils
import cv2

image = cv2.imread('7.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

blurred = cv2.blur(gradient, (9, 9))

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
blurred = cv2.erode(blurred, kernel, iterations = 4)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))
blurred = cv2.dilate(blurred, kernel, iterations = 4)

(_, thresh) = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 5))
closed = cv2.dilate(closed, kernel, iterations = 4)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
closed = cv2.erode(closed, kernel, iterations = 2)

cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cnts = imutils.grab_contours(cnts)

for i in range(len(cnts)):
    if cv2.contourArea(cnts[i]) > 2000:
        cv2.drawContours(image, cnts, i, (255, 0, 0), 3)
        
cv2.imwrite('s.jpg', image)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()