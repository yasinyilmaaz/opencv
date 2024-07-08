import cv2
import numpy as np

img =cv2.imread("opencv/4_contours/media/star.png")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,127,255,0)

contours,_ = cv2.findContours(thresh,2,1)
cnt = contours[0]

hull =cv2.convexHull(cnt, returnPoints = False) # çizginin dışındaki noktaları bulur
defects = cv2.convexityDefects(cnt,hull) # kusurları bulur

for i in range(defects.shape[0]):
    s, e, f, d = defects[i,0] # s: başlangıç, e: bitiş, f: uzaklık, d: kusur
    start = tuple(cnt[s][0]) # başlangıç noktası
    end = tuple(cnt[e][0]) # bitiş noktası
    far = tuple(cnt[f][0]) # uzaklık noktası
    cv2.line(img,start,end,[0,255,0],2)
    cv2.circle(img,far,5,[0,255,0],-1)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()