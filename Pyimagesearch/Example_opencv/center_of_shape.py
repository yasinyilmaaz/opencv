import argparse
import imutils
import cv2
# şeklin konturlarının merkezini bulma

"""
1. körüntüyü gri tonlara dönüştürelecek
2. gürültüleri azaltmak için bulanıklaştırma
3. kenar algılama ve eşikleme
"""

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path yhe input image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# KONTUR ALGILAMA KULLANARAK BEYAZ BÖLGELERİN YERİNİ BULUNACAK
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# cnts = sorted(cnts, key= cv2.contourArea, reverse=True)


for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.drawContours(image, [c], -1, (0, 255, 0), 2) # konturları çizer
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1) #merkezine daire koyar
    cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
