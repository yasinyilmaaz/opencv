import cv2
import numpy as np 


# Bu fonksiyon cv2.createTrackbar fonksiyonu için boş bir fonksiyona gerek var
def nothing():
    pass

img = np.zeros((700,512,3),np.uint8)
cv2.namedWindow("image")

# Renk değerlerini almak için barlar oluşturduk
cv2.createTrackbar("R","image", 0, 255, nothing)
cv2.createTrackbar("G","image", 0, 255, nothing)
cv2.createTrackbar("B","image", 0, 255, nothing)
switch= "0:OFF, 1:ON"
cv2.createTrackbar(switch,"image", 0, 1, nothing)

# Anlık olark değiştirmek için while döngüsüne aldık
while True:
    cv2.imshow("image", img)
    # Çıkış için atama yaptık
    if cv2.waitKey(1) & 0XFF == ord("q"):
        break
    # anlık olaarak barlardaki değerleri aldık
    r= cv2.getTrackbarPos("R", "image")
    g= cv2.getTrackbarPos("G", "image")
    b= cv2.getTrackbarPos("B", "image")
    s = cv2.getTrackbarPos(switch, "image")
    # swicth değerine göre açma ve kapama yaptık
    if s == 0:
        img[:] = [0,0,0]
    else:
        img[:]= [b, g, r]
cv2.destroyAllWindows()

