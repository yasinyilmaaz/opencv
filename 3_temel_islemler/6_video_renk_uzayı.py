import cv2
import numpy as np

# Videoların Renk Uzaylarını Değiştirme

# error: (-215:Assertion failed) size.width>0 && size.height>0 in function 'cv::imshow'
# Böyle bir hata herhangi bir video veya görselin olmadığını söyler
# Bunun için video yolunu tekrar kontrol edin
cap = cv2.VideoCapture(r"C:\Users\Yasin\Desktop\opencv\opencv\3_temel_islemler\media\antalya.mp4")

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


    cv2.imshow("video", frame)
    if cv2.waitKey(30) & 0XFF ==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()