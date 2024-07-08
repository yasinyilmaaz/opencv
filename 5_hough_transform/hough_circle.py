import cv2
import numpy as np

img1=cv2.imread(r"C:\Users\Yasin\Desktop\opencv\opencv\5_hough_transform\media\coins.jpg")
img2=cv2.imread(r"C:\Users\Yasin\Desktop\opencv\opencv\5_hough_transform\media\balls.jpg")

gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

img1_blur = cv2.medianBlur(gray1,5)
img2_blur = cv2.medianBlur(gray2,5)
# img2.shape[0]/4 --> daireler arası uzaklık 
# Radius= yarıçap
circles = cv2.HoughCircles(img1_blur,cv2.HOUGH_GRADIENT,1,img2.shape[0]/3,param1=200,param2=10,minRadius=25,maxRadius=70)  # 1: dp, 50: minDist, 200: param1, 10: param2, 15: minRadius, 70: maxRadius

if circles is not None:
    circles = np.uint16(np.around(circles))
    for a,i in enumerate(circles[0,:]):
        a = a+1
        cv2.circle(img1, (i[0],i[1]), i[2], (0,255,0),2)

cv2.imshow("img",img1)

cv2.waitKey(0)
cv2.destroyAllWindows()