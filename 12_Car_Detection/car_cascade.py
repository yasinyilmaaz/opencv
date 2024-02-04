import cv2
import numpy as np
# OpenCV ile araba algılamaya çalıştık ama yeterli olmadı


path_img= 'C:\\Users\\Yasin\\Desktop\\opencv\\12_Car_Detection\media\\car.jpg'
path_cascade = 'C:\\Users\\Yasin\\Desktop\\opencv\\12_Car_Detection\Haar_Cascade\\car.xml'


img = cv2.imread(path_img)
car_cascade = cv2.CascadeClassifier(path_cascade)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cars = car_cascade.detectMultiScale(gray,1.1,1)

for (x,y,w,h) in cars:
	cv2.rectangle(img,(x,y),(x+w,x+h),(0,0,255),3)
    
cv2.imshow('image',img)

cv2.waitKey()
cv2.destroyAllWindows()