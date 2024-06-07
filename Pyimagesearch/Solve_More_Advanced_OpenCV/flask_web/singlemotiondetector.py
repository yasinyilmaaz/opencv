import numpy as np
import cv2
import imutils

# Haraket algılama uygulamasının bulunacağı alan
# Algoritmanın kendisi yalnızca tek ve en büyük hareket
# bölgesini bulmakla ilgilendiği için buna "single motion detector" diyoruz.

class SingleMotionDetector:
    def __init__(self,accumWeight=0.5):
        # accumWeight ne kadar büyük olursa, ağırlıklı 
        # ortalama toplanırken arka plan (bg) o kadar az hesaba katılacaktır.
        # 0.5 değeri default olarak verilir. Duruma göre değer değiştirilebilir
        self.accumWeight = accumWeight
        self.bg = None
    
    def update(self, image):
        if self.bg is None:
            # bg çerçevenin yok olması durumunda(güncellemenin olmadğı durumda) bg çerçevesi saklanır.
            
            self.bg = image.copy().astype("float")
            return
        
        # verileri biriktirerek arka plan modelini günceller.
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)
        
    def detect(self, image, tVal=25):
        # tVal = Belirli bir pikseli "hareket" olarak işaretlemek veya işaretlememek için kullanılan eşik değeri.
        delta = cv2.absdiff(self.bg.astype("uint8"), image) # görüntü ile bg arasındaki mutlak farkı hesaplar
        # fark > tVal olan piksel konumları beyaz diğerleri siyah olarak işaretlenir(kısaca thresh metodu)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
        
        # Gürültüler temizlendi
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # Bu değişkenler bize hareketin gerçekleştiği yerin konumunu söyleyecek olan "sınırlayıcı kutuyu" oluşturacaktır.
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)
        
        # Listenin boş olup ulmadığını kontrol ediyoruz
        if len(cnts) == 0:
            return None
        
        for c in cnts:
            # tüm hareketin gerçekleştiği minimum ve maksimum (x, y) koordinatlarını bularak defter tutma değişkenlerimizi güncelleriz
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + w), (max(maxY, y + h)))
            
        return ( thresh, (minX, minY, maxX, maxY))
        