import cv2
import numpy as np

cap = cv2.VideoCapture('opencv/opencv/4_contours/media/dog.mp4')

while 1:

	_,frame = cap.read()
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	sensitivity = 15 # duyarlılık
	lower_white = np.array([0,0,255-sensitivity]) # beyazın alt sınırı
	upper_white = np.array([255,sensitivity,255]) # beyazın üst sınırı
	mask = cv2.inRange(hsv,lower_white,upper_white) # beyazı alır
	res = cv2.bitwise_and(frame,frame,mask=mask) # beyaz olan yerleri alır
	
	cv2.imshow("frame",frame)
	cv2.imshow("mask",mask)
	cv2.imshow("result",res)
	
	k = cv2.waitKey(20) & 0xFF
	if k == 27:
		break
	

cv2.destroyAllWindows()