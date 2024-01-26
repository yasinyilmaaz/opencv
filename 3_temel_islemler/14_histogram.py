import cv2
import numpy as np
from matplotlib import pyplot as plt
# Histogram grafiği BGR değerleri ile ilgili bilgi verir

# img = np.zeros((500, 500),np.uint8) + 50
# cv2.rectangle(img,(0,60),(200,150),(255,255,255),-1)
# cv2.rectangle(img,(250,170),(350,200),(255,255,255),-1)
# img = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/smile.jpg")
# görüntünün BGR değerlerini ayırır ve verir


# cv2.imshow("img",img)
# Histogram grafiğini çizer
# img.ravel() --> img değerlerini tek satıra dönüştürür
# değerler
# değer aralığı
# plt.hist(img.ravel(),256,[0,256])
# Gösterir
# plt.show()

img = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/media/smile.jpg")
b,g,r = cv2.split(img)
cv2.imshow("img",img)
plt.hist(b.ravel(),256,[0,256])
plt.hist(g.ravel(),256,[0,256])
plt.hist(r.ravel(),256,[0,256])
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()