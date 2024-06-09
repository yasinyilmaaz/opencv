import cv2
import numpy as np
import imutils
import pytesseract

# Araba sayfa uygulaması

path ="opencv\\17_Car_Counting\\media\\traffic.avi"

cap = cv2.VideoCapture(path)
# arkaplan çıkartmak için kullanılan fonksiyon
backsub = cv2.createBackgroundSubtractorMOG2()
c = 0

while 1:
    ret, frame = cap.read()

    if ret == False:
        False

    # Arkaplanı çıkartır
    fgmask = backsub.apply(frame)
    # BU çizgilerden araba geçerse sayacı bir artıracağız
    cv2.line(frame,(50,0),(50,300),(0,255,0),2)
    cv2.line(frame,(70,0),(70,300),(0,255,0),2)

    contours,hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    try: hierarchy = hierarchy[0]
    except: hierarchy= []

    for contour,hier in zip(contours,hierarchy):
        (x,y,w,h) = cv2.boundingRect(contour)
        # gelen konumlar belli bir büyüklükten büyük isekare içine alıyoruz
        if w > 40 and h > 40:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            if x > 50 and x <70:
                c+=1
    
    cv2.putText(frame,"car: " + str(c),(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)

    cv2.imshow("car counting", frame)
    cv2.imshow("fgmask", fgmask)

    if cv2.waitKey(30) & 0XFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()