import cv2
import numpy as np
# Göz algılama uygulaması
# ilk olarak yüzü algılayacağız
# daha sonra o bölgeyi ayırıp gözleri algılayacağız

path_cascade_eye ="C:\\Users\\Yasin\\Desktop\\opencv\\opencv\\10_Eye_Detection\\haar_detection\\haarcascade_eye.xml"
path_cascade_face ="C:\\Users\\Yasin\\Desktop\\opencv\\opencv\\10_Eye_Detection\\haar_detection\\frontalface.xml"
path_img = "C:\\Users\\Yasin\\Desktop\\opencv\\opencv\\10_Eye_Detection\\media\\eye.png"

img = cv2.imread(path_img)
face_cascade = cv2.CascadeClassifier(path_cascade_face)
eye_cascade = cv2.CascadeClassifier(path_cascade_eye)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray,1.3,7)

for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w,y+h),(0,0,255),3)

img2 = img[y:y+h,x:x+w]
gray2 = gray[y:y+h,x:x+w]

eyes = eye_cascade.detectMultiScale(gray2,1.3,4)

for (ex,ey,ew,eh) in eyes:
    cv2.rectangle(img2,(ex,ey), (ex+ew,ey+eh), (0,255,0),3)

cv2.imshow("image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()