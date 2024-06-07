"""
Seam Carving algoritması, tüm görüntüyü soldan sağa veya yukarıdan aşağıya 
kat eden düşük enerjili (yani en az önemli) dikiş adı verilen bağlantılı 
pikselleri bularak çalışır.
Bu dikişler daha sonra orijinal görüntüden kaldırılarak en göze çarpan
bölgeler korunurken görüntüyü yeniden boyutlandırmamıza olanak tanır.

Dikişler:soldan sağa veya yukarıdan aşağıya doğru akan bağlı pikseller olarak tanımlanır.
Seam Carving dört girdi alır
1. işlenecek görüntü
2. Enerji haritası: görüntünün en belirgin bölgelerini temsil etmelidir
    a. gradyan büyüklüğü gösterimi
    b. entropi haritaları
    c. belirginlik haritaları
3. yön (yatay veya dikey)
4. kaldıralacak dikiş sayısı
"""
# from skimage import transform,filters
import skimage # type: ignore
import cv2
import argparse
# Çalışmada hata var bakılacak!!!!!!!!!!!

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image file")
ap.add_argument("-d", "--direction", type=str, default="vertical", help="seam removal direction") # Oyma yönünü varsayılan olarak dikey
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# sobel = gradyan büyüklüğünü hesaplar
# Bu enerji haritası olacak
mag = filters.sobel(gray.astype("float"))

cv2.imshow("Orginal", image) 


for numSeams in range(20, 140, 20):
    carved = skimage.transform.seam_carve(image, mag, args["direction"],numSeams)
    print("[INFO] removing {} seams; new size: w={}, h={}".format(numSeams, carved.shape[1],carved.shape[0]))
    
    cv2.imshow("Carved", carved)
    cv2.waitKey(0)



