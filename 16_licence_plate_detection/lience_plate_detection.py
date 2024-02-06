import cv2
import numpy as np
import pytesseract
import imutils

# Araç plakası okuma uygulaması 

path = "C:\\Users\\Yasin\\Desktop\\opencv\\16_licence_plate_detection\\media\\licence_plate.jpg"
img = cv2.imread(path)
img = cv2.resize(img,(720,640))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Yumuşatma uygulayarak keskin hatları yumuşatıyoruz
filtered = cv2.bilateralFilter(gray,6,250,250)
edged = cv2.Canny(filtered,30,200)

contours = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# Uygun kontur değerlerini alır
cnts = imutils.grab_contours(contours)
# alana göre büyükten küçüğe doğru sıralama
cnts = sorted(cnts, key= cv2.contourArea,reverse=True)[:10]

screen = None

for c in cnts:
    # cv2.arcLength = konturların yay uzunluğunu bulur
    epsilon = 0.018*cv2.arcLength(c, True) # doğruluk katsayısı
    approx = cv2.approxPolyDP(c,epsilon,True) # konturları birbirine yakınlaştırıyor
    # approx1   4 değer varsa yani dikdörtgense
    if len(approx) == 4:
        screen = approx
        break

mask = np.zeros(gray.shape, np.uint8)
new_img = cv2.drawContours(mask,[screen],0,(255,255,255),-1)
new_img = cv2.bitwise_and(img,img,mask=mask)

# mask içinden beyaz alanları aldık
(x,y) = np.where(mask == 255)
# Bu alanların sol üst köşe ve sağ alt köşelerin kordinatlarını aldık
(topx,topy) = (np.min(x),np.min(y))
(bottomx,bottomy) = (np.max(x),np.max(y))
# Bu değerleri kırptık
cropped = gray[topx:bottomx+1,topy:bottomy+1]

text = pytesseract.image_to_string(cropped, lang="eng")
print(text)





cv2.imshow("licence plate",edged)
cv2.waitKey(0)
cv2.destroyAllWindows()