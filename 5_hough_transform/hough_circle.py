import cv2
import numpy as np

img1=cv2.imread("opencv/5_hough_transform/media/coins.jpg")
img2=cv2.imread("opencv/5_hough_transform/media/balls.jpg")

gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

img1_blur = cv2.medianBlur(gray1,5)
img2_blur = cv2.medianBlur(gray2,5)
# img2.shape[0]/4 --> daireler arası uzaklık 
# Radius= yarıçap
circles = cv2.HoughCircles(img2_blur,cv2.HOUGH_GRADIENT,1,img2.shape[0]/4,param1=200,param2=10,minRadius=15,maxRadius=70)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(img2, (i[0],i[1]), i[2], (0,255,0),2)

cv2.imshow("img",img2)

cv2.waitKey(0)
cv2.destroyAllWindows()