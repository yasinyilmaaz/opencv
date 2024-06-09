import cv2
import numpy as np
# Renk Uzaylarını Dönüştürme

# Bu resim BGR
img = cv2.imread(r"opencv\3_temel_islemler\media\klon.jpg")

# BGR TO RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# BGR TO HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# BGR TO GRAY
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



cv2.imshow("klon BGR", img)
cv2.imshow("klon HSV", img_hsv)
cv2.imshow("klon gray", img_gray)
cv2.imshow("klon RGB", img_rgb)


cv2.waitKey(0)
cv2.destroyAllWindows()