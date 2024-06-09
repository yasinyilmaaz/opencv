import cv2
import numpy as np
# Bit düzeyine mantıksal operatörleri kullanıcağız
# 0 --> siyah
# 1 --> beyaz

img1 = cv2.imread("opencv/3_temel_islemler/media/bitwise_1.png")
img2 = cv2.imread("opencv/3_temel_islemler/media/bitwise_2.png")

# Bit düzeyinde and komutu
# 0 ve 1 = 0
bit_and =cv2.bitwise_and(img1,img2)
# Bit düzeyinde or komutu
# 0 veya 1 = 1
bit_or =cv2.bitwise_or(img1,img2)
# XOR aynı ise sıfır farklı ise 1 verir
bit_xor =cv2.bitwise_xor(img1,img2)
# Not tam tersini alır
bit_not =cv2.bitwise_not(img1)
bit_not2 =cv2.bitwise_not(img2)



# cv2.imshow("bit_and",bit_and)
# cv2.imshow("bit_or",bit_or)
# cv2.imshow("bit_xor",bit_xor)
cv2.imshow("bit_not",bit_not)
cv2.imshow("bit_not2",bit_not2)
cv2.imshow("img1",img1)
cv2.imshow("img2",img2)


cv2.waitKey(0)
cv2.destroyAllWindows()