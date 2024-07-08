import cv2
import numpy as np
# Kenarları belirleme

img = cv2.imread(r'C:\Users\Yasin\Desktop\opencv\opencv\4_contours\media\contour.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

_,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
# konturları belirler
contours,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # cv2.RETR_TREE --> hiyerarşik konturlar, cv2.CHAIN_APPROX_SIMPLE --> konturları sadeleştirir
print(contours)
# çizer
# -1 --> hem ekranın hem cizmin konturlarını çizer
# 0 --> sadece ekranın konturlarını çizer
cv2.drawContours(img,contours,-1,(0,0,255),3)

cv2.imshow("contour",img)

cv2.waitKey(0)
cv2.destroyAllWindows()