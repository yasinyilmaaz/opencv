import cv2
import numpy as np
# Göz bebeği takibi

cap = cv2.VideoCapture("opencv/6_uygulama/media/eye_motion.mp4")

while 1:
    ret, frame = cap.read()
    if ret is False:
        break

    # frame = cv2.resize(frame,(640,480)) 
    roi = frame[80:210,230:450]
    rows, cols,_ = roi.shape
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # BINARY =  siyaha yakın yerleri simsiyah yapar
    # BINARY_INV = siyah olan yerler beyaz olur
    _,thershold = cv2.threshold(gray,3,255, cv2.THRESH_BINARY_INV)
    controus,_ = cv2.findContours(thershold, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # konturların alan büyüklüğüne göre tersten sıralar 
    controus = sorted(controus, key=lambda x:cv2.contourArea(x),reverse=True)

    # en büyük konturde işlem yapmak için bir kere döndürdük
    for cnt in controus:
        # dikdörtgenin sol üst ve yükseklik ve genişliği
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(roi, (x,y), (x+w, y+h),(255,0,0),2)
        cv2.line(roi, (int(x+(w/2)),0),(int(x+(w/2)),rows),(0,255,0),2)
        cv2.line(roi, (0,int(y+(h/2))),(cols,int(y+(h/2))),(0,255,0),2)
        break
    
    # Tüm görüntüyü görmek için roi üzerinde işlem yaptığımız 
    # değerleri frame ile birleştiriyoruz
    frame[80:210,230:450] = roi

    cv2.imshow("roi",roi)
    cv2.imshow("frame",frame)


    if cv2.waitKey(70) & 0xFF==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()