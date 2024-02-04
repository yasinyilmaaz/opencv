import cv2
import numpy as np
# Opencv ile insan vücudu bulma videoda

path_video = "C:\\Users\\Yasin\\Desktop\\opencv\\opencv\\11_Body_detection\\media\\body.mp4"
path_cascade = "C:\\Users\\Yasin\\Desktop\\opencv\\opencv\\11_Body_detection\\Haar_Cascade\\fullbody.xml"

cap = cv2.VideoCapture(path_video)
body_cascade = cv2.CascadeClassifier(path_cascade)



while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray,1.1,2)

    for (x,y,w,h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),3)
    
    cv2.imshow("Frame", frame)

    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()