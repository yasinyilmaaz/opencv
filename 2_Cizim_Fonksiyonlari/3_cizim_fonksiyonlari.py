import cv2
import numpy as np

img = np.zeros((512,512,3), dtype=np.uint8)

# çizgi
#  (tuval, başlangıç değeri, bitiş değeri, renk , kalınlık)
cv2.line(img,(50,50),(512,512), (255,0,0),thickness=5)
cv2.line(img,(100,50),(200,250), (0,0,255),thickness=7)

cv2.rectangle(img,(20,20),(50,50),(0,255,0), thickness=2)
# içi dolu dikdörtgen
# thickness değerine -1 bir verildiğinde içi dolu hal alır
cv2.rectangle(img,(20,20),(50,50),(0,255,0), thickness=-1)

# Çember oluşturma
cv2.circle(img, (250,250), 100, (0,0,255), thickness=4)

#  üçgen oluşturma (özel bir metod yok)
# cv2.line(img, (10,510), (40,480), (0,255,0),4)
# cv2.line(img, (40,480), (70,510), (0,255,0),4)
# cv2.line(img, (10,510), (70,510), (0,255,0),4)

p1 = (10,510)
p2 = (40,480)
p3 =(70,510)

cv2.line(img, p1, p2, (0,255,0),4)
cv2.line(img, p2, p3, (0,255,0),4)
cv2.line(img, p1, p3, (0,255,0),4)

# polylines
# cv2.polylines(tuval, konumlar, kapaı bir şekil için True, renk, kalınlık)
point = np.array([[[110,200], [330, 200], [290, 220], [220,250]]], np.int32)
# cv2.polylines(img, [point], True, (255,255,200),4)
cv2.polylines(img, [point], False, (255,255,100),4)

# ellipse
# cv2.ellipse(tuval, konum, (Xr,Yr), yataydaki açı, başlangıç derecesi, bitiş derecesi, renk, kalınlık)
cv2.ellipse(img, (300,300), (100,50), 0, 0,360, (255,255,0),-1)

cv2.imshow("canvas", img)
cv2.waitKey(0)
cv2.destroyAllWindows()