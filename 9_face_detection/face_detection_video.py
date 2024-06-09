import cv2
import numpy as np
# videodaki yüzleri algılama
path_cascade = "opencv/9_face_detection/haar_detection/frontalface.xml"
path_video = "opencv/9_face_detection/media/faces.mp4"

cap = cv2.VideoCapture(path_video)
face_cascade = cv2.CascadeClassifier(path_cascade)


while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,2)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    
    cv2.imshow("image",frame)


    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()