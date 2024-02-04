import cv2
import numpy as np

# Arka plan çıkarma manuel
# ilk frame ile karşılaştıralacak
# aynı olan yerler siyaha farklı olan yerler beyaza boyanacak

cap = cv2.VideoCapture("C:/Users/Yasin/Desktop/opencv/opencv/6_uygulama/media/car.mp4")
# ilk frame alıyoruz
ret, first_frame = cap.read()
cv2.resize(first_frame,(640,480))
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_blur = cv2.GaussianBlur(first_gray,(5,5),0)


while 1:
    ret, frame = cap.read()
    cv2.resize(frame,(640,480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Karşılaştırma işlemi yapacağız
    diff = cv2.absdiff(first_blur,blur)
    _,diff =cv2.threshold(diff, 25,255,cv2.THRESH_BINARY)

    cv2.imshow("frame",frame)
    cv2.imshow("diff",diff)

    if cv2.waitKey(20) & 0XFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()