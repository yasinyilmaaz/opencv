import cv2

img = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/klon.jpg")

# istediğimiz boyutlarda resmi ayarlamak için kullanırız
img = cv2.resize(img, (640,480))

cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows() 