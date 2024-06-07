import cv2
import imutils
import argparse
# OpenCV şekiş algılama

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
            # kontur yaklaşımı, bir eğrideki nokta sayısını azaltılmış bir nokta kümesi ile azaltmaya yönelik bir algoritmadır
            # Kontur yaklaşımı, bir eğrinin bir dizi kısa doğru parçasıyla yaklaştırılabileceği varsayımına dayanır.
            # Bu, orijinal eğri tarafından tanımlanan noktaların bir alt kümesinden oluşan yaklaşık bir eğri elde edilmesine yol açar.

            shape = "unidentified"
            peri = cv2.arcLength(c, True) # konturun çevresini hesaplar
            # ikinci parametresi için ortak değerler normalde orijinal kontur çevresinin %1-5 aralığındadır
            approx = cv2.approxPolyDP(c, 0.04 * peri, True) # kontur yaklaşımı uygulanır

            # yaklaşılan konturun kaç kenarı varsa ona göre şekil belirliyoruz
            if len(approx) == 3:
                shape = "triangle"
            
            elif len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

            elif len(approx) == 5:
                shape = "pentagon"
            else:
                shape =" circle"
            
            return shape
        

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.resize(image, (600,600))
resized = imutils.resize(image, width=600)
# eski yüksekliğin yeni boyutlandırılmış yüksekliğe oranını takip ediyoruz
ratio = image.shape[0] / float(resized.shape[0])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred= cv2.GaussianBlur(gray, (5,5), 0)

thresh = cv2.threshold(blurred, 60,255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
sd = ShapeDetector()
cv2.imshow("sd",thresh)
for c in cnts:

    # Kontur merkezini hesaplanır
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"] * ratio)
    cY = int(M["m01"] / M["m00"] * ratio)
    shape = sd.detect(c)

    # kontur merkezini yeniden boyutlandırma oranı ile çarpılır
    c= c.astype("float")
    c *= ratio
    c = c.astype("int")

    # konturlar çizilir
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # ÇIKTI
    cv2.imshow("Image", image)
    cv2.waitKey(0)

# Hu momentleri şekil tanımlayıcısıdır. Hu momentleri,
# cv2.HuMoments işlevi aracılığıyla OpenCV kütüphanesine yerleştirilmiştir. 
    
# Daha sonra, Hu momentlerinden yola çıkarak araştırma ve çalışma üzerine inşa edilen Zernike momentlerine sahibiz.
# Zernike momentlerinin uygulanmasının sonucu, görüntüdeki şekli ölçmek için kullanılan 25 sayıdan oluşan bir listedir.
# Zernike momentleri Hu momentlerinden biraz daha güçlü olma eğilimindedir ancak bazı manuel parametre ayarlamaları gerektirebilir