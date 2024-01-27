import cv2
import numpy as np

# Klavyeden girilen tuş ile o ankiakan klavyeden frameleri kaydeden kod
# Kod çalışırken eğer "h" basılırsa o andaki akan frameleri kaydeder

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    
    if ret == 0:
        break

    frame = cv2.flip(frame, 1)

    cv2.imshow("frame", frame)

    if cv2.waitKey(20) & 0XFF == ord("h"):
        cv2.imwrite("img1.jpg",frame)


    if cv2.waitKey(20) & 0XFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()