import cv2
import numpy as np
# Fare ile tıklandığında görüntüde diskler oluşturma


cap = cv2.VideoCapture(0)
circles = []
def mouse(event,x,y,flags, params):
    # sol tuşa basıldı ise
    if event == cv2.EVENT_LBUTTONDOWN:
        circles.append((x,y))

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse)

while 1:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame,(640,480))

    for center in circles:
        cv2.circle(frame, center,20,(255,0,0),-1)
    
    cv2.imshow("Frame",frame)

    

    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

    if cv2.waitKey(20) & 0xFF==ord('h'):
        circles = []

cap.release()
cv2.destroyAllWindows()