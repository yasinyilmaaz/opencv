import cv2
import numpy as np
# Resim dönüşüm uygulaması

def nothing(x):
    pass

path1 = "opencv/7_uygulama/media/aircraft.jpg"
path2 = "opencv/7_uygulama/media/ball.jpg"

img1 = cv2.imread(path1)
img1 = cv2.resize(img1, (640,480))
img2 = cv2.imread(path2)
img2 = cv2.resize(img2, (640,480))

output = cv2.addWeighted(img1,0.5,img2,0.5,0)

windowName = "Transition Program"
cv2.namedWindow(windowName)

cv2.createTrackbar("Alpha-Beta",windowName,0,1000,nothing)

while True:
    cv2.imshow(windowName,output)
    alpha = cv2.getTrackbarPos("Alpha-Beta",windowName)/1000
    beta =1- alpha
    output = cv2.addWeighted(img1,alpha,img2,beta,0)

    print(alpha,beta) 

    if cv2.waitKey(20) & 0xFF==ord('q'):
        break


cv2.destroyAllWindows()







cv2.waitKey(0)
cv2.destroyAllWindows()