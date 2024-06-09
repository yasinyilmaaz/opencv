import cv2
import numpy as np

path_cascade = "opencv/9_face_detection/haar_detection/frontalface.xml"


cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(path_cascade)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # cascade dosyası kullanarak her bir kare üzerindeki yüzlerin koordinatlarını bulur
    faces = face_cascade.detectMultiScale(gray, 1.6,4)

    # Bu kordinatlar ile o noktaları kare içine alırız
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("image", frame)


    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

