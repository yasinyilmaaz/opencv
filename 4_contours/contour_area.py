import cv2
# Alan ve çevre hesaplama
img = cv2.imread(r"opencv\4_contours\media\contour.png")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255,cv2.THRESH_BINARY) # 127 den büyük olanları beyaz yapar
contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # cv2.RETR_TREE: hiyerarşik kontur bulma, cv2.CHAIN_APPROX_SIMPLE: konturun sadeleştirilmesi

cnt = contours[0]
# Alanını verir
area = cv2.contourArea(cnt) 
print("alan: ",area)

M = cv2.moments(cnt)
print(M['m00'])
# çevresini verir
perimeter = cv2.arcLength(cnt,True) # True: kapalı mı değil mi
print("Çevresi: ",perimeter)


"""

cv2.imshow("original",img)
cv2.imshow("gray",gray)
cv2.imshow("thresh",thresh)


cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""