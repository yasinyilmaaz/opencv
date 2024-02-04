import cv2
import numpy as np

# erezyon yöntemi 

img = cv2.imread("C:/Users/Yasin/Desktop/opencv/opencv/3_temel_islemler/media/klon.jpg",0) 
kernel = np.ones((5,5), np.uint8)
# Görüntüyü bozar
erosion = cv2.erode(img,kernel,iterations=1)
# Kalınlaştırma
dilation = cv2.dilate(img,kernel,iterations=1)
# Gürültü = resim üzerindeki gereksiz duran noktalar
# Resimdeki gürültüleri kaldırmış
opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

# ŞEKİLDEKİ UYUMSUZLUKLAR veya GÜRÜLTÜLER GİDİRİLİR 
close = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
# kenar çizgileri daha belli olur
gradient = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)

tophat = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)
blackhat = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)





cv2.imshow("img", img)
cv2.imshow("opening-OPEN", opening)
cv2.imshow("opening-CLOSE", close)
cv2.imshow("opening-gradient", gradient)
# cv2.imshow("erosion", erosion)
# cv2.imshow("dilation", dilation)


cv2.waitKey(0)