from __future__ import print_function
import numpy as np
import cv2
path= "opencv\\Mission\\media\\many3.jpeg"

image = cv2.imread(path)
image = cv2.resize(image, (1280,980))
shifted = cv2.pyrMeanShiftFiltering(image, 21, 81)


gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

kernel = np.ones((11,11),np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,kernel, iterations = 1)
cv2.imshow("Thresh", opening)

dist = cv2.distanceTransform(opening, cv2.DIST_L2, 3)

ret, dist1 = cv2.threshold(dist, 0.5*dist.max(), 255, 0)


markers = np.zeros(dist.shape, dtype=np.int8)
dist_8u = dist1.astype('uint8')
contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
many = len(contours)
cv2.putText(image,f"{many} tane para",(20,40),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,255))
for i in range(len(contours)):
    cv2.drawContours(markers, contours, i, (i+1), -1)

markers = cv2.watershed(image, markers)
image[markers == -1] = [0,0,255]


cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()