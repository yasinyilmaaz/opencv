import cv2
import numpy as np

# Arka plan çıkarma mod


cap = cv2.VideoCapture(r"C:\Users\Yasin\Desktop\opencv\opencv\6_uygulama\media\car.mp4")
# detectShadows=True ==> Gölgeleride tespit eder    
# history=100 ==> alınan frame sayısı
subtractor = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=50,detectShadows=True)

while 1:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640,500))
    mask = subtractor.apply(frame)

    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)

    if cv2.waitKey(20) & 0XFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()