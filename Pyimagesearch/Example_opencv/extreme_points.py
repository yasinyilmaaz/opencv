import imutils
import cv2

# OpenCV ile konturlardaki uç noktaları bulma

image = cv2.imread("pyimagesearch\\Example_opencv\\media\\extreme_points_input.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)

# el bölgesini geri kalan yerlerden ayrılır
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None,iterations=2)

# Konturları bulduk
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key= cv2.contourArea, reverse=True)
c = max(cnts, key=cv2.contourArea) # en büyük konturluyu seçiyoruz

# x değeri üzerinden argmin() tarafından döndürülen indeksle ilişki rüm (x,y) kordinatları alarak en küçük x değerli yani en sol değeri buluruz
# diğerleride aynı şekilde diğer en leri bulur
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

# elin etrafı sarı ile çizildi
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
"""
Batı'ya: Kırmızı
Doğu: Yeşil
Kuzey: Mavi
Güney: Deniz mavisi
"""
cv2.circle(image, extLeft, 8, (0,0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
