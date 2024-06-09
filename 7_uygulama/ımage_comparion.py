import cv2
import numpy as np
# Resimleri karşılaştırma

path1 ="opencv/7_uygulama/media/aircraft.jpg"
path2 ="opencv/7_uygulama/media/aircraft2.jpg"



img1 = cv2.imread(path1)
img1 = cv2.resize(img1, (640,480))

img2 = cv2.imread(path2)
img2 = cv2.resize(img2, (640,480))

img3 = cv2.medianBlur(img1,7)

# Boyutlarını karşılaştırma
# if img1.shape == img2.shape:
#     print("Same size")
# else:
#     print("bot same")

# diff = difference
# iki resimde farklı olan yerlerin rengini değiştirir
diff = cv2.subtract(img1,img3)
b,g,r = cv2.split(diff)

# cv2.countNonZero(b) => sıfıra eşit olmayan değerleri bulur
if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
    print("Completely equal")
else:
    print("Not Completely equal")

cv2.imshow("img1",img1)
cv2.imshow("img2",img2)
cv2.imshow("difference",diff)
cv2.waitKey(0)
cv2.destroyAllWindows()
