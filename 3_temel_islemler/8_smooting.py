import cv2
import numpy as np
# Resim Yumuşatma demek


img_filter = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/media/filter.png")
img_median = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/media/median.png")
img_bilateral = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/media/bilateral.png")

# (5,5)Resmin yumuşama değeri ==> değerleri pozitif tek sayılar olması gerekir
blur = cv2.blur(img_filter, (5,5))
blur_g= cv2.GaussianBlur(img_filter, (5,5),cv2.BORDER_DEFAULT)
blur_m = cv2.medianBlur(img_median,11) 

blur_b = cv2.bilateralFilter(img_bilateral,9,95,95)


# cv2.imshow("blur", blur)
# cv2.imshow("blur_g", blur_g)
cv2.imshow("blur_b", blur_b)
# cv2.imshow("Orginal", img_filter)
cv2.imshow("Orginal", img_bilateral)


cv2.waitKey(0)
cv2.destroyAllWindows()