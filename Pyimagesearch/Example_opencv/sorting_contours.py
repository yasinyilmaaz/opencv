import numpy as np
import cv2
import argparse
import imutils
# Python ve OpenCV Kullanarak Konturları Sıralama


# Önce her bir konturun sınırlayıcı kutularını hesaplarız,
#  bu basitçe sınırlayıcı kutunun başlangıç (x, y) koordinatları ve ardından genişlik ve yüksekliktir

# dışardan alınan argumanlar
# cnts = sıralamak istediğimiz konturlar
# method = sıralanma sitili
def sort_contours(cnts, method="left-to-right"):
    reverse = False # sıralama düzeni
    i = 0 #sınırlayıcı kutunun indexsi

    # tersten sıralama için
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # eksen seçimi (x,y)
    if  method =="top-to-bottom" or method == "bottom-to-top":
        i=1
    
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    # hem konturları hem de sınırlayıcı kutuları sağladığımız kriterlere göre sıralayabiliyoruz.
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts,boundingBoxes), key= lambda b : b[1][i], reverse=reverse))

    return (cnts, boundingBoxes)

# konturları çizer
# image, kontur, i= eksen bilgisi
def draw_contour(image, c, i):

    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    return image

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="Path to the input image")
ap.add_argument("-m","--method", required=True, help="Sorting metod")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
accumEdged = np.zeros(image.shape[:2], dtype="uint8")

# kenar haritası oluturur yani konturleri çıkarır
# görüntünün her bir Mavi, Yeşil ve Kırmızı kanalı üzerinde döngü yaparız,
# yüksek frekanslı gürültüyü gidermek için her bir kanalı hafifçe bulanıklaştırırız
for chan in cv2.split(image):
    chan = cv2.medianBlur(chan, 11)
    edged = cv2.Canny(chan, 10, 100) # kenarları algılar
    accumEdged = cv2.bitwise_or(accumEdged, edged) # kenar haritasını güncelleriz

cv2.imshow("Edge Map", accumEdged)

# Konturları bulur
cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4] # boyutuna (büyükten küçüğe) göre sıralar
orig = image.copy()

# sıralanmış konturları döndürüyoruz (boyut açısından, konum açısından değil)
for (i, c) in enumerate(cnts):
    orig = draw_contour(orig, c, i)

cv2.imshow("Unsorted", orig)
#  sırasıyla sıralanmış sınırlayıcı kutular ve konturlardan oluşan bir tuple döndürür
(cnts,boundingBoxes) = sort_contours(cnts, method=args["method"])

for (i,c) in enumerate(cnts):
    draw_contour(image, c, i)

cv2.imshow("Sorted", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

