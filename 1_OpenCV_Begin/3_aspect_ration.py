import cv2

# Verdiğimiz boyut değerine göre resmimizin orantılı bir boyut almasını sağlayan fonksiyon

def resizeWidthAspectRatio(img, width= None, height= None, inter= cv2.INTER_AREA):
    
    dimension = None
    (h, w)= img.shape[:2]

    # Eğer iki değer de girilmemiş ise o boyutlara göre yapar
    if width is  None and height is None:
        return img
    # Eğer width değeri yoksa width değerini height değerine göre orantılar
    elif(width is None):
        r = height / float(h) # oranı bulur
        dimension = (int(w*r),height)
    # Eğer height değeri yoksa height değerini width değerine göre orantılar
    else:
        r = width / float(w)
        dimension = (int(h*r),width)

    return cv2.resize(img, dimension,interpolation=inter)

img = cv2.imread("C:/Users/Yasin/Desktop/opencv/3_temel_islemler/klon.jpg")
img1 = resizeWidthAspectRatio(img, width=None,height=600,inter= cv2.INTER_AREA)

# cv2.imshow("Orginal", img)
cv2.imshow("Resized", img1)

cv2.waitKey(0)
cv2.destroyAllWindows()