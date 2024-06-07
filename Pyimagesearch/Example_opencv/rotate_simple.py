import numpy as np 
import argparse
import imutils
import cv2

# Döndürme işlemleri

# manuel olarak kırpılmadan döndürme
def rotate_bound(image, angle):
    (h,w) = image.shape[:2]
    # Merkez kordinatlarını aldı
    (cX,cY) = (w // 2, h // 2)

    # Merkez etrafında döndürdü
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    # Döndürme sırasıda oluşan cos ve sin değerlerini aldı
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    
    # Bu değerleri en boy uzunluklarına uygulayarak resmin ekrana sığmayan kısımlarınıda gözükmesini sağlayacak
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    
    # Dönüş matrisini değiştirerek öteleme işlemini gerçekleştirdi
    M[0, 2] += (nW / 2) -cX
    M[1, 2] += (nH / 2) -cY
    
    # Görüntüyü döndürdü ve resmin kesilmeden görünmesini sağladı
    return cv2.warpAffine(image, M, (nW, nH))








ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

# loop over the rotation angles
# resmi (0,360) arasında 15 derece artarak döndürüyoruz
for angle in np.arange(0,360,15):
    # resim döndükçe ekranın büyüklüğü değişmez  
    rotated = imutils.rotate(image,angle)
    cv2.imshow("Rotated (problematic)", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    


# loop over the rotation angles again, this time ensuring
# no part of the image is cut off
for angle in np.arange(0,360,15):
    # resim döndükçe ekran büyüklüğü köşelere göre ayarlanır
    # rotated = imutils.rotate_bound(image, angle)
    rotated = rotate_bound(image, angle)
    cv2.imshow("Rotated (Corrrect)", rotated)
    cv2.waitKey(0)

    cv2.destroyAllWindows()