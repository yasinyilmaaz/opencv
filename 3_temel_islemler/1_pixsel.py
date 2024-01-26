import cv2
import numpy as np

img = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/media/klon.jpg")
# img boyutları kanal verisini verir
dimession = img.shape
print(dimession)

# görüntünün belirttiğimiz konumdaki değerleri
# color = img[1000,1000]
# print(color)
# img[row,col,index]
blue = img[420,500,0]
print(blue)

green = img[420,500,1]
print(green)

red = img[420,500,2]
print(red)

img[420, 500, 0] = 250
print("new blue: ", img[420,500,0])

blue1 = img.item(150, 200, 0)
print("blue1: ", blue1)

img.itemset((150,200,0), 172)
print("new blue1: ", img[150, 200, 0])

cv2.imshow("Klon Asker", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
