import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
font2 = cv2.FONT_HERSHEY_COMPLEX

img = cv2.imread("opencv/6_uygulama/media/polygons.png")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)

contours, _ =cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    epsilon = 0.01*cv2.arcLength(cnt,True)
    # konturları bulduk
    approx = cv2.approxPolyDP(cnt,epsilon,True)

    cv2.drawContours(img, [approx],0 ,(0),5)

    # x ve y kordinatlarını aldık
    x = approx.ravel()[0]
    y = approx.ravel()[1]

    # Uzunluğunu alıp ona göre kaçgen olduğunu yazdırız
    if len(approx) == 3:
        cv2.putText(img,"Triangle", (x,y),font,1,0)
    elif len(approx) == 4:
        cv2.putText(img,"Rectangle", (x,y),font,1,0)
    elif len(approx) == 5:
        cv2.putText(img,"Pentagon", (x,y),font,1,0)
    elif len(approx) == 6:
        cv2.putText(img,"Hexagon", (x,y),font,1,0)
    elif len(approx) > 6:
        cv2.putText(img,"Ellipse", (x,y),font,1,0)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()