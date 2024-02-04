import cv2
import numpy as np

# çözünürlük değerlerini ayarlama
windowName = "Live Video"

cv2.namedWindow(windowName)

cap = cv2.VideoCapture(0)

# cap.get(3) => width
# cap.get(4) => height

print("width: " + str(cap.get(3)))
print("height: " + str(cap.get(4)))

# yeni çözünürlük değerleri
cap.set(3,1280)
cap.set(4,720)

print("width*: " + str(cap.get(3)))
print("height*: " + str(cap.get(4)))


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.imshow(windowName, frame)

    if cv2.waitKey(30) & 0xFF==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()