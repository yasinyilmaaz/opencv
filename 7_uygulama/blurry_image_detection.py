import cv2
import numpy as np
# Bir resmin blurlu olup olmadığına bakma

path1 ="C:/Users/Yasin/Desktop/opencv/opencv/7_uygulama/media/starwars.jpg"

img = cv2.imread(path1)
blurry_img = cv2.medianBlur(img, 7)

laplacian =cv2.Laplacian(blurry_img,cv2.CV_64F).var()
print(laplacian)

if laplacian < 500:
    print("blurry image")

# cv2.imshow("img",img)
# cv2.imshow("b_img",blurry_img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()