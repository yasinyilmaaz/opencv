# roi --> region of interest -->ilgi alanı
# İstenilen bölge
import cv2

img = cv2.imread(r"opencv\3_temel_islemler\media\klon.jpg")
# En boy oranını çekildi
print(img[:2])
# Resmindeki askerin kafasının bulunduğu aralık alındı
roi = img[30:200, 200:360]

cv2.imshow("ROİ",roi)

cv2.imshow("klon", img)
cv2.waitKey(0)
cv2.destroyAllWindows()