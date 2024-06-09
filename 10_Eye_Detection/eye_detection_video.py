import cv2
import numpy as np


path_video = "opencv\\10_Eye_Detection\\media\\eye.mp4"
path_cascade_eye ="opencv\\10_Eye_Detection\\haar_detection\\haarcascade_eye.xml"
path_cascade_face ="opencv\\10_Eye_Detection\\haar_detection\\frontalface.xml"

cap = cv2.VideoCapture(path_video)
face_cascade = cv2.CascadeClassifier(path_cascade_face)
eye_cascade = cv2.CascadeClassifier(path_cascade_eye)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,480))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,7)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),3)

        roi_frame = frame[y:y+h,x:x+w]
        roi_gray = gray[y:y+h,x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_frame, (ex,ey), (ex+ew,ey+eh), (0,90,75),3)


    cv2.imshow("Frame",frame)

    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()