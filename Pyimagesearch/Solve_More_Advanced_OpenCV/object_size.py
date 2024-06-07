from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# Görüntüdeki nesnelerşn boyutunu ölçme
"""
Bu nesnenin boyutlarını (genişlik veya yükseklik açısından) ölçülebilir bir birim olarak (milimetre, inç vb.) bilmeliyiz.
Bu referans nesneyi, ya nesnenin yerleşimine göre yadarengine göre ayırt edebilmemiz gerekir

pixels_per_metric = 150px / 0.955in = 157px

Bu da görüntümüzde her 0,955 inç başına yaklaşık 157 piksel düştüğü anlamına gelir.
Bu oranı kullanarak bir görüntüdeki nesnelerin boyutunu hesaplayabiliriz.


"""

def midpoint(ptA, ptB):
    return((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1])*0.5)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-w", "--width", type=float,required=True, help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
image = imutils.resize(image, width=400)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7,7), 0)

# Daha sonra kenar haritasındaki kenarlar arasındaki boşlukları kapatmak için bir 
# genişletme + erozyon ile birlikte kenar algılama gerçekleştiriyoruz
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)


cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

for c in cnts: 
    
    # kontur istenen büyüklükte değilse atlanır
    if cv2.contourArea(c) < 100:
        continue
    
    orig = image.copy()
    box = cv2.minAreaRect(c)
    # sınırlayıcı kutusunu hesaplanır
    box = cv2.boxPoints(box) if imutils.is_cv2 else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
    
    for (x,y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
    
    (tl, tr, br, bl) = box
    # ardından sol üst ve sağ üst noktalar arasındaki orta nokta
    (tltrX, tltrY) = midpoint(tl, tr)
    # ardından sağ alt noktalar arasındaki orta nokta
    (blbrX, blbrY) = midpoint(bl, br)
    
    (tlblX, tlblY) = midpoint(tl, bl) #  sol üst + sol alt
    (trbrX, trbrY) = midpoint(tr, br) # sağ üst + sağ alt
    
    #  satırlar görüntümüzün mavi orta noktalarını çizer ve ardından orta noktaları mor çizgilerle birleştirir
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
    
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)
    
    # orta nokta kümelerimiz arasındaki Öklid mesafesini hesaplar
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    
    if (pixelsPerMetric is None):
        pixelsPerMetric = dB / args["width"] # inç başına (yaklaşık) piksellerimiz
        
    # ilgili Öklid mesafelerini pixelsPerMetric değerine bölerek nesnenin boyutlarını (inç cinsinden) hesaplar
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric
    
    
    cv2.putText(orig, "{:.1f}in".format(dimA), (int(tltrX -15), int(tltrY -10)),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(orig, "{:.1f}in".format(dimB), (int(trbrX -10), int(trbrY)),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    
    cv2.imshow("Image", orig)
    cv2.waitKey(0)
    
