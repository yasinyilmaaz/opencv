import cv2
import numpy as np
# Görüntüdeki Paraları tespit eden ve kaç tane olduğunu yazan kod
path= "C:\\Users\\Yasin\\Desktop\\opencv\\opencv\\Mission\\media\\many3.jpeg"

# path= "media\\many2.jpeg"

img = cv2.imread(path)
img = cv2.resize(img, (720,640))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.medianBlur(gray,21)

edge = cv2.Canny(img_blur,175,90)

kernel = np.ones((2,2), np.uint8)
sure_bg = cv2.dilate(edge,kernel, iterations=1)

unknown= cv2.subtract(sure_bg,edge)

ret, markers = cv2.connectedComponents(edge)
markers = markers+1
markers[unknown==255] = 0
markers = cv2.watershed(img, markers)
dist_8u = markers.astype('uint8')

circles = cv2.HoughCircles(dist_8u,cv2.HOUGH_GRADIENT,1,img.shape[0]/4.5,param1=200,param2=10,minRadius=45,maxRadius=120) 

if circles is not False:
    circles = np.uint16(np.around(circles))
    many =str(len(circles[0,:]))
    cv2.putText(img,f"{many} tane para",(20,40),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,255))
    for i in circles[0,:]:
        cv2.circle(img, (i[0],i[1]), i[2], (0,255,0),2)
        cv2.circle(img, (i[0],i[1]),2,(0,255,0),-1 ) 


cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()