import cv2
import numpy as np
# Opencv ile insan vücudu bulma

path_img = "opencv\\11_Body_detection\\media\\body.jpg"
path_cascade = "opencv\\11_Body_detection\\Haar_Cascade\\fullbody.xml"

img = cv2.imread(path_img)
body_cascade = cv2.CascadeClassifier(path_cascade)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

body = body_cascade.detectMultiScale(gray,1.1,1)

for (x,y,w,h) in body:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),3)

# Hiçbir şey Bulamadık
# Bunun nedeni insan vücüduna benzer çok şey olması

cv2.imshow("ismage",img)

cv2.waitKey(0)
cv2.destroyAllWindows()