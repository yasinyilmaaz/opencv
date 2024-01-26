import cv2
import numpy as np

# f(x,y) = x*a + y*b + c
# a = ilk resmin yüzde yoğunluğu
# b = ikinci resmin yüzde yoğunluğu
# C = sabit bir sayı


circle = np.zeros((512,512,3), np.uint8) + 255
cv2.circle(circle, (256, 256), 60, (255, 0, 0), -1)

rectangle = np.zeros((512,512, 3), np.uint8) + 255
cv2.rectangle(rectangle, (150, 150), (350, 350), (0, 0, 255), -1)

# Ağırlıklı toplama 
dst = cv2.addWeighted(circle,0.3,rectangle,0.7, 11)

cv2.imshow("Circle", circle)
cv2.imshow("rectangle", rectangle)
cv2.imshow("DST", dst)



cv2.waitKey(0)
cv2.destroyAllWindows()