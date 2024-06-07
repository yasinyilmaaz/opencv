# The Color Transfer Algorithm
# 1. adım: Bir hedef bir kaynak görüntü alınacak
# 2. adım: Hem kaynak hem de hedef görüntüyü L*a*b* renk uzayına dönüştürün.RGB renk uzayına göre daha iyi iş çıkarır
# 3. adım: görüntünün renklerini kanallarına ayıralım
# 4. adım: (kaynak ve hedef görüntülerin)L*a*b* kanalın ortalamasını ve standart sapmasını hesaplayalım
# 5. adım: Hedef görüntünün L*a*b* kanallarının ortalamasını hedef kanallardan çıkaralım
# 6. adım: Hedef kanalları, hedefin standart sapmasının kaynağın standart sapmasına bölünmesi ve hedef kanallarla çarpılması oranına göre ölçeklendirilir.
# 7. adım: kaynak için L*a*b* kanalların ortalaması eklenir
# 8. adım: [0,255] arasında olmayan değerleri kırpılır
# 9. adım: kanallar tekrar birleştirilir.
# 10. adım: renk uzayını RGB renk uzayına göre dönüştürülür

import numpy as np
import cv2
import argparse

def image_Stats(image):
    # L*, a* ve b* kanallarının her biri için piksel yoğunluklarının ortalamasını ve standart sapmasını hesaplanır

    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    return (lMean, lStd, aMean, aStd, bMean, bStd)

# kaynak görüntüden hedef görüntüye renk aktarımını gerçekleştircek
def color_transfer(source, target):

    # standart RGB yerine L*a*b* renk uzayı kullanılacaktır
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # OpenCV görüntüleri çok boyutlu NumPy dizileri olarak temsil eder, ancak varsayılan olarak uint8 veri türünü kullanır. Bu çoğu durum için iyidir,
    # ancak renk aktarımını gerçekleştirirken potansiyel olarak negatif ve ondalık değerlere sahip olabiliriz, bu nedenle kayan nokta veri türünü kullanmamız gerekir.
    

    # image_Stats() = L*, a* ve b* kanallarının her biri için piksel yoğunluklarının ortalamasını ve standart sapmasını hesaplanır
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_Stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_Stats(target)

    # hedef görüntüyü L*, a* ve b* bileşenlerine ayırır ve ilgili ortalamalarını çıkarırız
    (l,a,b)= cv2.split(target)
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    # hedef standart sapmanın kaynak görüntünün standart sapmasına oranıyla ölçeklendirir
    # 6. adım
    l = (lStdTar / lStdSrc) * l
    a = (aStdTar / aStdSrc) * a
    b = (bStdTar / bStdSrc) * b

    # aynak kanallarının ortalamasını ekleyerek Adım 7'yi uygularız
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    #  [0, 255] aralığının dışında kalan değerleri kırpldı
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # L*a*b* kanallarını birleştirip RGB formatına dönüştürüldü
    transfer = cv2.merge([l,a,b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    # rengi aktarılmış görüntü geri döndürülür
    return transfer

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input directory of images")
# örnek çıktı sayısı. varsayılan olarak 21 değerindedir
ap.add_argument("-t", "--target", required=True,
	help="# of images to sample")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.resize(image, (512,512))
target = cv2.imread(args["target"])
target = cv2.resize(target, (512,512))
output = color_transfer(image,target)

cv2.imshow("output",output)
cv2.imshow("image",image)
cv2.imshow("target",target)
cv2.waitKey(0)
cv2.destroyAllWindows()