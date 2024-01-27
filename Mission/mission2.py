import cv2
import numpy as np

# hsv renk uzayı ile kendi belirlediğin bir nesneyi tespit ettirmek
# yeşil renkli cisimlerin tespit edilmesi

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_color = np.array([44, 98, 137])
    upper_color = np.array([97, 255, 255])
    
    mask = cv2.inRange(frame_hsv,lower_color,upper_color)
    contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    hull = []

    for i in range(len(contours)):
        hull.append(cv2.convexHull(contours[i],False))
    
    for i in range(len(contours)):
        cv2.drawContours(frame,hull,i,(255,0,0),2,10)

    # merkez göstermek için
    _,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
    try:
        M = cv2.moments(thresh)

        x = int(M["m10"]/M["m00"])
        y = int(M["m01"]/M["m00"])

        cv2.circle(frame,(x,y),5,(0,255,0),-1)
    except:
        pass

    cv2.imshow("Yesil Kalem", frame)

    if cv2.waitKey(20) & 0XFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
