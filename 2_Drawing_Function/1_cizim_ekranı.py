import cv2
import numpy as np

# Burda siyah bir tuval oluşturduk
# ilk olarak boyutlarını belirledik 
# np.uint8 ise veri tipini belirtir
# 3 kanal verisi renkli resimler için geçerlidir
# siyah beyaz resimlerde bu yoktur

canvas = np.zeros((512,512,3),dtype=np.uint8) + 100
# print(canvas) => bgr (255,255,255) beyaz

cv2.imshow("canvas", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()