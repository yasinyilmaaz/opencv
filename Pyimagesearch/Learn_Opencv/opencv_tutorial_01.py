# gerekli paketleri içe aktar
import imutils
import cv2

# giriş görüntüsünü yükleyin ve boyutlarını gösterin
# görüntüler, çok boyutlu bir NumPy dizisi olarak temsil edilir.
# şekil no. satır (yükseklik) x. sütunlar (genişlik) x . kanallar (derinlik)
image = cv2.imread("pyimagesearch/Learn_Opencv/media/jp.jpg")
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h, d))
# görüntüyü ekranımıza görüntüleyin - pencereyi tıklamamız gerekecek
# OpenCV tarafından açılır ve yürütmeye devam etmek için klavyemizdeki bir tuşa basın


# OpenCV görüntüleri RGB yerine BGR düzeninde saklar

(B, G, R) = image[100, 50]
print("R={}, G={}, B={}".format(R, G, B))

# Veriyi kırpma 
# Verideki istediğimiz bölgesini almak için kullanırız
# veri[y:y,x:x]
roi = image[100:200, 320:420]

cv2.imshow("roi",roi)


# Yeniden Boyutlandırma
resized = cv2.resize(image, (200,200))
cv2.imshow("resize(200,200)",resized)

cv2.imshow("Resim", image)
cv2.waitKey(0)