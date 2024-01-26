import cv2 
import numpy as np
# Görüntünün yönünü değiştirme

img = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/media/klon.jpg",0)
row, col = img.shape 
# ((merkez noktaları),döndürülme miktarı,ölçek)
M = cv2.getRotationMatrix2D((col/2,row/2),90,1)

dst = cv2.warpAffine(img,M,(col,row))

cv2.imshow("dst",dst)
cv2.waitKey(0)
