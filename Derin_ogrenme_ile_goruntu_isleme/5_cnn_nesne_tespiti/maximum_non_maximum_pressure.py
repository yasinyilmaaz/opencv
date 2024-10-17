import numpy as np
import cv2

def non_maxi_suppression(boxes, probs=None, overlapThresh=0.3):
    #overlapThresh: kutuların ne kadar örtüşebileceğini belirleyen eşik değeri ayarlarnır
    print(boxes)
    print("AAA")
    # kutu seçimi yapama durumunda boş liste döndürüyor
    if boxes.size == 0:
        return []
    if boxes.dtype.kind == "i": # gele nkutunun veri tipi int ise floata çeviriyoruz.
        boxes = boxes.astype("float")

    x1 = boxes[:, 0] # kutuların x1 koordinatları (sol üst)
    y1 = boxes[:, 1] # kutuların y1 koordinatları (sol üst)
    x2 = boxes[:, 2] # kutuların x2 koordinatları (sağ alt)
    y2 = boxes[:, 3] # kutuların y2 koordinatları (sağ alt)

    area = (x2 - x1 +1) * (y2 - y1 +1)  # kutuların alanları hesaplanır

    idxs = y2 # kutuların y2 koordinatlarından indexler oluşturulur

    # olasılık değerleri

    if probs is not None:
        idxs = probs
    
    idxs = np.argsort(idxs) # indexler küçükten büyüğe sıralanır

    pick = [] # kutuların seçileceği liste oluşturulur

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # en büyük ve en küçük x ve y değerleri bulunur

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # w, h, bul

        w = np.maximum(0, xx2- xx1 + 1)
        h = np.maximum(0, yy2- yy1 + 1)

        # overlap oranı hesaplanır

        overlap = (w * h) / area[idxs[:last]]

        # overlap oranı eşik değerinden altında olan kutuları listeden çıkarır

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")





