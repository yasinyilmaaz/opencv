import cv2
import numpy as np
# Elimizdeki şablonu görüntü içinde bulma

path1 = "C:/Users/Yasin/Desktop/opencv/opencv/7_uygulama/media/starwars.jpg"
path2 = "C:/Users/Yasin/Desktop/opencv/opencv/7_uygulama/media/starwars2.jpg"

img1 = cv2.imread(path1)
gray_img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

template = cv2.imread(path2,cv2.IMREAD_GRAYSCALE)
# yükseklik, genişlik
w,h = template.shape[::-1]

# şablonu bulma
result = cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
# print(result)

location = np.where(result >=0.9)

# zip(*location[::-1]) =>anlamlı bir veri haline getirdik
for point in zip(*location[::-1]):
    cv2.rectangle(img1,point,(point[0]+w,point[1] +h),(0,255,0),3)


cv2.imshow("Image", img1)

cv2.waitKey(0)
cv2.destroyAllWindows()
