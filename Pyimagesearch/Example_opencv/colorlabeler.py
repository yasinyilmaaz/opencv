from scipy.spatial import distance as dist
from collections import OrderedDict
from shapedetector import ShapeDetector
import numpy as np
import argparse
import imutils
import cv2
# OpenCV ile nesne rengini belirleme
# color_histogram_and_color_channel_statistics sayfası incelenebilir
"""
* renk histogramı 
* standart sapma
Neden L*a*b* renk uzayını kullanıyoruz?
Bir görüntünün belirli bir renk içeren bölgelerini
etiketlemek için bilinen renklerden oluşan veri kümemiz
ile belirli bir görüntü bölgesinin ortalamaları arasındaki Öklid mesafesini hesaplayacağız.
Öklid mesafesini en aza indiren bilinen renk, renk tanımlaması olarak seçilecektir.
HSV ve RGB renk uzaylarının aksine, L*a*b*
renkleri arasındaki Öklid mesafesinin gerçek bir algısal anlamı vardır 
"""


# Görüntülerdeki renkleri etiketleme
class ColorLabels:
    def __init__(self):
        # Renk sözlüğü
        colors = OrderedDict({
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0)
        })

        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        # renk adları
        self.colorNames= []

        for (i, (name, rgb)) in enumerate(colors.items()):
            # L*a*b* dizisini ve renk adları listesinde güncelleme
            self.lab[i] = rgb
            self.colorNames.append(name)

        # L*a*b* dizisini RGB renk uzayından dönüştürür
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_BGR2LAB)
    
    def label(self, image, c):
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        # yalnızca maskelenmiş bölge için görüntünün L*, a* ve *b* kanallarının her birinin ortalamasını hesaplar.
        mean = cv2.mean(image, mask=mask)[:3]

        # şimdiye kadar bulunan minimum mesafeyi başlatır
        minDist = (np.inf, None)

        # lab dizisinin her satırı üzerinde döngü yaparak bilinen her renk ile ortalama renk arasındaki Öklid mesafesini hesaplar
        for (i, row) in enumerate(self.lab):
            d = dist.euclidean(row[0], mean)
            # en küçük Öklid mesafesine sahip rengin adını döndürür.
            if d < minDist[0]:
                minDist = (d, i)

        return self.colorNames[minDist[1]]


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])


blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]


cnts = cv2.findContours(thresh.copy(), cv2. RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts= imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
sd = ShapeDetector()
cl = ColorLabels()

for c in cnts:

    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"] * ratio)
    cY = int(M["m01"] / M["m00"] * ratio)

    shape = sd.detect(c)
    color = cl.label(lab, c)

    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    print(color)
    text = "{} {}".format(color, shape)
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

"""
L*a*b* renk uzayını ve Öklid mesafesini kullanarak genellikle küçük renk kümelerini tanımlayabilirsiniz,
ancak daha büyük renk paletleri için bu yöntem,
görüntülerinizin karmaşıklığına bağlı olarak muhtemelen yanlış sonuçlar verecektir.
"""