import cv2
import imutils

img = cv2.imread("pyimagesearch/Learn_Opencv/media/jp.jpg")
(h, w, d) = img.shape

# Verinin merkez noktası
center = (w // 2, h // 2)
# resmi merkez noktasını alarak sola doğru döndürme
M = cv2.getRotationMatrix2D(center, -45, 1.0)
rotated = cv2.warpAffine(img, M, (w,h))
# imutils ile aynı işlemi daha az kod ile yapabiliriz
rotated2 = imutils.rotate(img, -45)
# Resmi kırpmadan gösterir
rotated2 = imutils.rotate_bound(img, 45)
cv2.imshow("OpenCV Rotation2", rotated2)
cv2.imshow("OpenCV Rotation", rotated)
cv2.waitKey(0)