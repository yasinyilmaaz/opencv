import cv2
import numpy as np

img = np.zeros((512,512,3), dtype=np.uint8) + 255

# fontlar
font1 = cv2.FONT_HERSHEY_COMPLEX
font2 = cv2.FONT_HERSHEY_SIMPLEX
font3 = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
# (tuval, yazı, konum, font, boyut, renk, ddd)
cv2.putText(img, "Yasin",(50,100),font2,3,(0,0,0),cv2.LINE_AA)


cv2.imshow("canvas", img)
cv2.waitKey(0)
cv2.destroyAllWindows()