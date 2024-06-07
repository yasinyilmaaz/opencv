from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
# yedi sekmentli ekranda görüntü algılama
# Hata 3 ü 9 olarak algılıyor

"""
 ___________
/  __0____  \
|1|_______|2|
   \     /
   |  3  |
___/     \___
|4|_______|5|
\_____6_____/

"""
# Aşşağıdaki tabloda her biranahtar yukardaki 7 segmetasyonlu
# sıraya göre bir rakama denk gelmektedir
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1 ,0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}

image = cv2.imread(r"C:\Users\Yasin\Desktop\pyimagesearch\Solve_More_Advanced_OpenCV\media\termostat.jpg")

image = imutils.resize(image, height=500) # yeniden boyutlama
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # gri tona dönüştürme
blurred = cv2.GaussianBlur(gray, (5,5), 0) # görüntüdeki gürültüleri azaltmak için 5x5 kernel ile yumuşatma uygulandı
edged = cv2.Canny(blurred, 50, 200, 255) # kenar haritası çıkarıldı
cv2.imshow("Edged", edged)

# konturları bulundu ve büyükten küçüğe sıralandı
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

for c in cnts:
    
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
    if len(approx) == 4:
        displayCnt = approx
        break
# perspektif dönüşümü uygular
warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4,2))
cv2.imshow("Warped", warped)
cv2.imshow("output", output)

thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)


cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = [] # rakamların konturlarını saklayacak liste

for c in cnts:
    
    (x, y, w, h) = cv2.boundingRect(c)
    # konturların kabul edilebilir boytta olup olmadığına bakılır
    # eğer eğilse ayarlarda değişikliğe gidilebilir
    if w >= 15 and (h >= 30 and h <= 40):
        digitCnts.append(c)
    
# (x,y) kordinatlarına göre soldan sağa doğru sıralıyoruz
digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
digits = []

# her bir rakam konturu üstünde döngü başlatıldı
for c in digitCnts:
    
    (x, y, w, h) = cv2.boundingRect(c)
    roi = thresh[y:y+h, x:x+w] # heseplanan sınırlı kutular içersinde roiler çıkarıldı
    
    # roi nin yaklaşık genişliğini ve yüksekliğini hesaplar
    (roiH, roiW)= roi.shape
    (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
    DHC = int(roiH * 0.05)
    
    # 7 segmente karşılık gelen (x,y kordinatlarının listesi tanımlanır)
    segments = [
        ((0, 0), (w, dH)), # top
        ((0, 0), (dW, h // 2)), # top-left
        ((w - dW, 0), (w, (h // 2))), # top-right
        ((0, (h // 2) -DHC), (w, (h // 2) + DHC)), # center
        ((0, h // 2), (dW, h)), # bottom-left
        ((w- dW, h // 2), (w, h)), # bottom-right
        ((0, h- dH), (w, h)) # bottom
    ]
    # sekmentin kapalı olduğunu gösterir
    on = [0] * len(segments)
    
    for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
        segROI = roi[yA:yB, xA:xB] # roi
        total = cv2.countNonZero(segROI) # eşiklenmiş pikseller yani sıfır olmayan piksellerş hesaplanır
        area = (xB -xA) * (yB - yA) # segmentin alanı
        
        if total / float(area) > 0.5: #toplam alanına oranıyarısından fazla ise
            on[i] = 1 # segment açık olduğunu belirtiriz
    
    digit = DIGITS_LOOKUP[tuple(on)] # rakamın kendisini elde ederiz
    print(digit)
    digits.append(digit)
    # sayının etrafına bir dikdörtgen çizer
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
    # bulunan sayıyı yazar
    cv2.putText(output, str(digit), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    
print(u"{}{}.{} \n00b0C".format(*digits))
cv2.imshow("Input", image)
cv2.imshow("Output", output)  


cv2.waitKey(0)
cv2.destroyAllWindows()