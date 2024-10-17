import cv2
import numpy as np
import os

# Kamera Aç
cap = cv2.VideoCapture(0)

ret, frame = cap.read()

# Kamera açılamazsa hata mesajı ver
if ret == False: 
    print("KAMERA AÇILAMADI")

# detection
path = os.path.join(os.getcwd(),  "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(path)
face_rects = face_cascade.detectMultiScale(frame)

(face_x, face_y, w, h) = tuple(face_rects[0])
track_window = (face_x, face_y, w, h)

# region of interest
roi = frame[face_y:face_y+h, face_x:face_x+w] #roi = face
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0,180]) #Takip için histogramı ayarladık
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Takip için durdurma kriterleri
# count = hesaplanacak maksimum iterasyon sayısı
# epsilon = değişiklik miktarı
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if ret :
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # histogramı bir görüntüde bulmak için kullanıyoruz
        # Piksel değerlerine göre histogramı hesaplar ve karşılaştırır
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1) 
        
        # yeni konum bilgilerini döndürü
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)
        x,y,w,h = track_window

        img2 = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 5)

        cv2.imshow("Takip", img2)

        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()