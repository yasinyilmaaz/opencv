import numpy as np
import argparse
import imutils
import cv2
# Şekillerin ne olduğu ve merkezini bulma

# OpenCV'nin görüntüleri RGB yerine BGR düzeninde sakladığını unutmayın!!!!!!


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

# renk aralığımız siyah ile siyaha yakın tonları kapsıyor
lower = np.array([0, 0, 0])
upper = np.array([15, 15, 15])
# siyah renkleri tespit ediyoruz
shapeMask = cv2.inRange(image, lower, upper)

# Tüm dış konturlar bulundu
cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key= cv2.contourArea, reverse=True)
print("I found {} black shapes".format(len(cnts)))
cv2.imshow("Mask", shapeMask)

for c in cnts:
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)

