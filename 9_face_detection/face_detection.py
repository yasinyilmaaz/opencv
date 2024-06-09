import cv2
import numpy as np

path_cascade = "opencv/9_face_detection/haar_detection/frontalface.xml"
path_img = "opencv/9_face_detection/media/face.png"

img = cv2.imread(path_img)
face_cascade = cv2.CascadeClassifier(path_cascade)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# her bir karedeki yüzlerin kordinatlarını bulur
# (görüntü, ölçeklendirme,belirli bir bölgede bulunacak en az değer)
faces = face_cascade.detectMultiScale(gray,1.3,7)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(w+w,y+h),(0,0,255),2)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()


