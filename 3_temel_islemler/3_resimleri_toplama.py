import cv2
import numpy as np
# Renk değerlerinin toplanmasından oluşur

circle = np.zeros((512,512,3), np.uint8) + 255
cv2.circle(circle, (256,256), 60, (255,0,0), -1)

rectangle =  np.zeros((512,512,3), np.uint8) + 255
cv2.rectangle(rectangle, (150,150), (350,350), (0,0,255), -1)
cv2.imshow("circle", circle)
cv2.imshow("recagle", rectangle)

# İki resmmi toplamak için add komutunu kullanırız
# İki resmin boyutları eşit olmalı
add = cv2.add(circle,rectangle) 
cv2.imshow("add",add)

cv2.waitKey(0)
cv2.destroyAllWindows()