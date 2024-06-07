import cv2

# Resmi normal bir şekilde okur
img = cv2.imread("opencv/3_temel_islemler/klon.jpg")

# print(img) #Resimler renk yoğunlukarından oluşan matrikslerdir

# Resmi gri tonlarda okur 0 da yazılabilir
# img = cv2.imread("klon.jpg",cv2.IMREAD_GRAYSCALE)


cv2.namedWindow("image",cv2.WINDOW_NORMAL) # RESMİ boyutlandırılabilir hale getirdik


# Resmi gösterir
# ilk değer pencerenin adı ikinci resim
cv2.imshow("image",img)

# Resmi kaydetme
# cv2.imwrite("klon1.jpg",img)

# resmi ekranda tutar
# milisaniye cinsindendir
# 0 yazarsak bir tuşa basanakdar veya kapatana kadar ekranda tutar
cv2.waitKey(0)
# kapatırken tüm pencereleri kapatır
cv2.destroyAllWindows()
