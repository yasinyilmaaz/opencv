from __future__ import print_function
import imutils
import cv2
# OpenCV version kontolü 

print(f"OpenCv Version: {cv2.__version__}")
image = cv2.imread(r"Learn_Opencv\media\tetris_blocks.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]


if imutils.is_cv2() or imutils.is_cv4():
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
elif imutils.is_cv3():
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
cv2.drawContours(image, cnts, -1, (240, 0, 160), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()