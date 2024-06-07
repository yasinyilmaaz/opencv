from skimage.filters import threshold_local #taranmış görüntüye siyah beyaz izlenim vermeyi sağlar
import numpy as np
import argparse
import cv2
import imutils
from transform import four_point_transform
# OpenCV ile bir belge tarayıcısı oluşturmak

"""
1. Kenar tespiti
2. Kağıt kenarları tespiti
3. perspektif dönüşüm
"""

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image to be scanned")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

# Kenar vulma
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(gray, 75, 200)

print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Konturları bulma
#  görüntüde tam olarak dört noktaya sahip en büyük konturun taranacak kağıt parçası olduğunu varsayacağız.

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# konturları alana göre sıralamak ve yalnızca en büyük olanları tuttuk
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

for c in cnts:
    # nokta sayısını yaklaşık olarak hesaplae 
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        screenCnt = approx
        break

print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perspektif Dönüşümü ve threshold Uygula


#  çarpıtma dönüşümünü gerçekleştirir
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)


warped =cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset= 10, method="gaussian")
warped = (warped> T).astype("uint8") * 255

print("STEP 3: Apply perspective transform")

cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Warped", imutils.resize(warped, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()

"""

Bir başka harika "sonraki adım" da görüntüdeki belgelere OCR uygulamak olacaktır.
Sadece belgeyi tarayıp bir PDF oluşturmakla kalmaz,
aynı zamanda metni de düzenleyebilirsiniz!
"""