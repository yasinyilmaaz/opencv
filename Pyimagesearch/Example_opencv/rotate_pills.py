import numpy as np
import argparse
import imutils
import cv2
# Hapları döndürme 


ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3,3), 0)
edged = cv2.Canny(gray, 30, 80)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Kenar haritasında en az bir kontur bulunduğuna bakıyoruz
if len(cnts) > 0:
    # En büyük kontur noktası için bir mask oluşturuyoruz
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(gray.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # Sınırlayıcı bölgenin kordinatlarını bulduk
    (x,y,w,h) = cv2.boundingRect(c)
    # Asıl roi kısmını aldık
    imageROI = image[y:y + h, x: x+ w]
    maskROI = mask[y:y + h, x: x+ w]
    imageROI = cv2.bitwise_and(imageROI, imageROI, mask=maskROI)

    for angle in np.arange(0, 360, 15):
        rotated = imutils.rotate(imageROI,angle)
        cv2.imshow("Rotated (Problamatic)", rotated)
        cv2.waitKey(0)
    
    # Hiç hap kesilmeden görüntünün gözükmesini sağlar
    for angle in np.arange(0, 360, 15):
        rotated = imutils.rotate_bound(imageROI, angle)
        cv2.imshow("Rotated (Correct)", rotated)
        cv2.waitKey()

# cv2.imshow("image", maskROI)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
