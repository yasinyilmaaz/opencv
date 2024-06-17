import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread(r"C:\Users\Yasin\Desktop\opencv_2\bird.jpg")
img_type = type(img)
# print(img)
# print(img.shape) 
plt.imshow(img) # resim renkleri farklı gözükebilir
# bunun sebebi matplotlib RGB ve OpenCV BGR renk uzayında olduğu için
RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(RGB_img)

img_gray = cv2.imread(r"C:\Users\Yasin\Desktop\opencv_2\bird.jpg", cv2.IMREAD_GRAYSCALE) # tam olarak gray formatında değil
# plt.imshow(img_gray)
plt.imshow(img_gray, cmap="gray") # gri formatta
print(img_gray.min()) # min değeri
print(img_gray.max()) # max değeri
# plt.imshow(img_gray, cmap="magma")
resize_img = cv2.resize(RGB_img, (1200, 300)) # yeniden boyutlandırma
plt.imshow(resize_img)

h_ratio = 0.5
w_ratio = 0.5

new_img = cv2.resize(RGB_img, (0,0), RGB_img, w_ratio, h_ratio) # yarı boyutunda oranladık
plt.imshow(new_img)
print(RGB_img.shape) # normal
print(new_img.shape) # oraanlanmış
cd_img = cv2.flip(RGB_img, 0) # x ekseninde ters çevirir
plt.imshow(cd_img)
cd2_img = cv2.flip(RGB_img, 1) # y ekseninde ters çevirir
plt.imshow(cd2_img)
cd3_img = cv2.flip(RGB_img, -1) # hem x hem y ekseninde çevirir
plt.imshow(cd3_img)
# plt.show()

cv2.imwrite("new_bird.jpg", cd3_img)