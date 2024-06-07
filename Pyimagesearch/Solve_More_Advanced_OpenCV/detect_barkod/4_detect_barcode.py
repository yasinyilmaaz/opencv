import numpy as np
import argparse
import imutils
import cv2
# Barkod okuyucu

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# yatay ve dikey yönlerdeki gradyan büyüklüğü temsilini oluşturmak için Scharr operatörünü kullanılır
ddepth = cv2.CV_32F if imutils.is_cv2() else cv2.CV_32F
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0,ksize=-1)
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

# y gradyanını x gradyanından çıkarılır
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

blurred = cv2.blur(gradient, (9, 9))
(_,thresh) = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
cv2.imshow("ss",thresh)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7)) # dikey şeritleri arasındaki boşlukları kapatmamıza izin verir
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow("ww", closed)
# Lekeler kaldırıldı
closed = cv2.erode(closed, None, iterations=4)
closed = cv2.dilate(closed, None, iterations=4)
cv2.imshow("closed", closed)
cnts= cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

rect = cv2.minAreaRect(c)
box = cv2.cv.boxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
box = np.int0(box)


cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()