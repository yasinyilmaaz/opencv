import cv2
import imutils

image = cv2.imread("pyimagesearch/Learn_Opencv/media/jp.jpg")
(h, w, d) = image.shape

r = 300.0 / w

dim = (300, int(h *r))
resized = cv2.resize(image, dim)
resized = imutils.resize(image, width=300)
# cv2.imshow("Imutils Resize", resized)
cv2.imshow("Ascept Ratio Resize", resized)
cv2.waitKey(0)