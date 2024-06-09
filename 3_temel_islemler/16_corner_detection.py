import cv2
import numpy as np 

img = cv2.imread("opencv/3_temel_islemler/media/text.png")
img2 = cv2.imread("opencv/3_temel_islemler/media/contour.png")

gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# floata çevirdik
gray = np.float32(gray)
# (görüntü,bulunacak köşe sayısı, kalite,köşeler arası mesafe)
corners = cv2.goodFeaturesToTrack(gray,50,0.01,10)
# görüntüleyebilmek için tekrar int çevirdik
corners = np.int0(corners)

# kenar sayısını döndürür
for corner in corners:
    # kordinatlarını aldık
    x,y = corner.ravel()
    # o naoktalara nokta koyduk
    cv2.circle(img2,(x,y),3,(0,0,255),-1)

cv2.imshow("corner",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
    
