import cv2
import numpy as np
# Görüntüdeki Paraları tespit eden ve kaç tane olduğunu yazan kod

path= "C:\\Users\\Yasin\\Desktop\\opencv\\many.jpeg"

img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.medianBlur(gray,5)

circles = cv2.HoughCircles(img_blur,cv2.HOUGH_GRADIENT,1,img.shape[0]/6,param1=200,param2=10,minRadius=15,maxRadius=40) 

if circles is not False:
    circles = np.uint16(np.around(circles))
    # Kaç tane daire çizdiğini aldım
    many =str(len(circles[0,:]))
    # Kaç tane olduğunu yazdırdık
    cv2.putText(img,f"{many} tane para",(20,40),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,255))
    for i in circles[0,:]:
        cv2.circle(img, (i[0],i[1]), i[2], (0,255,0),2)


cv2.imshow("image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()