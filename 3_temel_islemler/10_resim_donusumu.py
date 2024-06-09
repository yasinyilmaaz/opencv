import cv2
import numpy as np

img = cv2.imread("opencv/3_temel_islemler/media/klon.jpg",0)
# satır ve sütun piksel sayıları
row,col  = img.shape

# [1, 0, 10] üçüncü değer belirtilen taraftaki siyah kısımları belirtiyor
M = np.float32([[1,0,10],[0,1,200]])
dst = cv2.warpAffine(img,M,(row,col))

cv2.imshow("dst",dst)
cv2.waitKey(0)
# cv2.destroyAllWindows()