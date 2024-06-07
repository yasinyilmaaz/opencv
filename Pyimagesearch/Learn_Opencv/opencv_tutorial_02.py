import cv2
import imutils
import argparse


ap = argparse.ArgumentParser()
ap.add_argument('-i', "--image", required=True, help="path to input image")
args = vars(ap.parse_args())
# Resim dosya yolunu alarak resmi çağırdık
image = cv2.imread(args["image"])
# Bir görüntüyü gri tonlamaya dönüştürme
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow("Gray",gray)

# Edge detection (Kenar Algılama)
# (gray img, mineşik değeri, max eşik değeri, Sobel çekirdek boyutu "varsayılan değeri 3")
edged= cv2.Canny(gray,30,50)
# cv2.imshow("Edged", edged)

# Thresholding 
# görüntülerin daha açık veya daha koyu bölgelerini ve konturlarını kaldırmamıza yardımcı olabilir.
thresh = cv2.threshold(gray, 225,255, cv2.THRESH_BINARY_INV)[1]
# 225 ten küçük değerleri 0 yani siyah yapar diğer yerleri 255 yani beyaz yapar
# cv2.imshow("Thresh", thresh)

# Detecting and drawing contours (Konturları algılama ve çizme)
# konturları tespit etmek için kullanılır
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts =imutils.grab_contours(cnts)
output = image.copy()

for c in cnts:
    cv2.drawContours(output, [c], -1, (240,0,159), 3)

text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text,(10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(240,0,159),2)


# cv2.imshow("Output", output)
# Erosions and dilations (Erozyonlar ve dilatasyonlar)
# Erozyonlar ve dilatasyonlar tipik olarak ikili görüntülerdeki gürültüyü azaltmak için kullanılır (eşiklemenin bir yan etkisi).
# mask = thresh.copy()
# mask = cv2.erode(mask, None, iterations=5)
# cv2.imshow("Eroded", mask)

mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)
cv2.imshow("Dilated", mask)

# Masking and bitwise operations (Maskeleme ve bitsel işlemler)
# Maskeler, bir görüntünün ilgilenmediğimiz bölgelerini "maskelememize" olanak tanır. Bunlara "maske" diyoruz çünkü görüntülerin önemsemediğimiz bölgelerini gizlerler.
mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Output", output)


cv2.imshow("Image", image)
cv2.waitKey(0)