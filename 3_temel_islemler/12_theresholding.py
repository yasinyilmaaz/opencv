import cv2
import numpy as np
# Resim öbekleme

img = cv2.imread("opencv/3_temel_islemler/media/klon.jpg",0) #grayscalc

ret, th1 = cv2.threshold(img,150,200,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)


# cv2.imshow("img",img)
cv2.imshow("img-TH1",th1)
cv2.imshow("img-TH2",th2)
cv2.imshow("img-TH3",th3)
cv2.waitKey(0)