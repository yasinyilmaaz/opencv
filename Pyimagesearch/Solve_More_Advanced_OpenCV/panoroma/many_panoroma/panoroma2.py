from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
# Birleştirelecek görüntülerin dizinine giden yol
ap.add_argument("-i","--images", type=str, required=True,help="path to input directory of images to stitc")
# Sonucun kaydedileceği çıktı görüntüsünün yolu
ap.add_argument("-o", "--output", type=str, required=True, help="path to the output image")
args = vars(ap.parse_args())

print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["images"]))) # Görüntüleri yükler ve sıralar

images = []
# magePath için görüntüyü yükler ve görüntüler listesine ekleriz
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
# hem bir durum hem de dikilmiş görüntüsünü döndürür
(status, stitched) = stitcher.stitch(images)

# Hata yok ise
if status == 0:
    cv2.imwrite(args["output"], stitched)
    
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
    
else:
    print("[INFO] image stitching failed ({})".format(status))

#  panoramayı çevreleyen şu siyah bölgeler
# panoramayı oluşturmak için gereken perspektif çözgülerinin gerçekleştirilmesinden kaynaklanmaktadır.



