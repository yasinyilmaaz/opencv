"""Histogram eşitleme, görüntünün histogramının piksel yoğunluğu dağılımını güncelleyerek bir görüntünün kontrastını iyileştirir
konstrast sınırlı uygulanabilir
Histogram eşitlemenin çalışma mantığı:
histogramda en büyük sayılara sahip olanları eşit şekilde yaymak için 
Kümülatif dağılım fonksiyonuna (CDF) doğrusal bir eğilim verir
Histogram eşitleme uygulamasının sonucu, daha yüksek global kontrasta sahip bir görüntü oluşur.

Gürültüyü arttırmadan histogram eşitlemek için:
Uyarlanabilir histogram eşitleme kullanılır. Bir giriş görüntüsünü M x N ızgaraya böleriz. Daha sonra ızgaradaki her 
hücreye eşitleme uygulayarak daha yüksek kaliteli bir çıktı görüntüsü elde ederiz
"""
import argparse
import cv2
# basic histogram equalization 

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
	help="path to the input image")
args = vars(ap.parse_args())

print("[INFO] loading input image...")
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("[INFO] performing histogram equalization...")
# Temel histogram eşitlemeyi kullandı
equalized = cv2.equalizeHist(gray)

cv2.imshow("Input", gray)
cv2.imshow("Histogram Equalization", equalized)
cv2.waitKey(0)
cv2.destroyAllWindows()