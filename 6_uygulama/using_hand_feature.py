import cv2
import numpy as np 
import math
# El konturu bulma
cap = cv2.VideoCapture(0)

# Görüntüdeki en bbüyük kontur alanını bulmak için olan fonksiyon
def findMacContour(contour):
    max_i = 0
    max_area = 0
    for i in range(len(contour)):
        area_hand = cv2.contourArea(contour[i])
        if max_area < area_hand:
            max_area = area_hand
            max_i= i
        try:
            c= contour[max_i]
        except:
            contour = [0]
            c = contour[0]
        return c
    

while 1:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    roi = frame[50:250,200:400]# frame[y1:y2,x1:x2]
    cv2.rectangle(frame,(200,50),(400,250),(0,0,255),0)

    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    lower_color = np.array([0,45,79], dtype=np.uint8)
    upper_color = np.array([17,255,255], dtype=np.uint8)

    mask = cv2.inRange(hsv,lower_color,upper_color)
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(mask,kernel,iterations=1)
    mask = cv2.medianBlur(mask, 13)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    
    if len(contours)>0:
        try:
            c= findMacContour(contours)
            # en küçük x değerlerini bularak konumlarını alacak
            extLeft = tuple(c[c[:,:,0].argmin()][0])
            extRight = tuple(c[c[:,:,0].argmax()][0])
            extTop = tuple(c[c[:,:,1].argmin()][0])
            extBotton = tuple(c[c[:,:,1].argmax()][0])

            # Bu noktalara birer daire koyuyoruz
            cv2.circle(roi,extLeft,5,(0,255,0),2)
            cv2.circle(roi,extRight,5,(0,255,0),2)
            cv2.circle(roi,extTop,5,(0,255,0),2)


            # Daireler birleştirildi
            cv2.line(roi,extLeft,extTop,(255,0,0),2)
            cv2.line(roi,extTop,extRight,(255,0,0),2)
            cv2.line(roi,extRight,extLeft,(255,0,0),2)


            # sağ köşedeki açıyı bulmak için
            a = math.sqrt((extRight[0]-extTop[0])**2+(extRight[1]-extTop[1])**2)
            c = math.sqrt((extTop[0]-extLeft[0])**2+(extTop[1]-extLeft[1])**2)
            b = math.sqrt((extRight[0]-extLeft[0])**2+(extRight[1]-extLeft[1])**2)
            try:
                angle_ab = int(math.acos((a**2+b**2-c**2)/(2*b*c))*57)
                if angle_ab > 70:
                    cv2.rectangle(frame,(0,0),(100,100),(255,0,0),-1)
                else:
                    pass

                cv2.putText(roi,str(angle_ab),(extRight[0]-100+50,extRight[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
            except:
                cv2.putText(roi,"?",(extRight[0]-100+50,extRight[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255,2,cv2.LINE_AA))




        except:
            pass
    else:
        pass



    cv2.imshow("frame",frame)
    cv2.imshow("roi",roi)
    cv2.imshow("mask",mask)

    if cv2.waitKey(20) & 0xFF==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()