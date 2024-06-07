import cv2
import imutils
# konvolüsyom işlemi = bulanıklaştırma veya yumuşatma

# Gerçekte, bir (görüntü) konvolüsyonu basitçe iki matrisin eleman çarpımı ve ardından bir toplamdır.

# Standart bir RGB görüntüsü için derinliğimiz 3'tür - sırasıyla Kırmızı, Yeşil ve Mavi kanalların her biri için bir kanal.

image = cv2.imread("pyimagesearch/Learn_Opencv/media/jp.jpg")

blurred = cv2.GaussianBlur(image, (11,11), 0)
cv2.imshow("blurred", blurred)


cv2.waitKey(0)