from imutils import paths
import argparse
import cv2
import imutils

# Blur tespit etme

# cv2.Laplacian(image, cv2.CV_64F).var()
# görüntü gri tonlarda alınır ve 3 x 3 kernel ile konvolüze edilir
# yanıtın varyansını (yani standart sapmanın karesini) alınır
# Varyans önceden tanımlanmış eşiğin altına düşerse bulanık değildir
"""
The Laplacian Kernel
----   ----
| 0  1  0 |
| 1 -4  1 |
| 0  1  0 |
----   ----
"""

# görüntünün odak ölçüsünü hesaplama
def variance_of_laplacian(image):
    # görüntüyü 3 x 3 Laplacian operatörü ile konvolize eder ve varyansı döndürür.
    return cv2.Laplacian(image, cv2.CV_64F).var()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to input directory of images")
# veri kümesine göre değişiklik gösterir
ap.add_argument("-t", "--threshold", type=float, default=100.0, help="focus measures that fall below this value will be considered 'blurry'") # bulanıklık testi için eşik değeri
args = vars(ap.parse_args())


for imagePath in paths.list_images(args["images"]):
    image = cv2.imread(imagePath)
    image = imutils.resize(image, height=600)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    text = "Not Blurry"
    
    if fm > args["threshold"]: # eşik değerinden büyük ise
        text = "Blurry"
    
    cv2.putText(image, "{}: {:.2f}".format(text,fm), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),3)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)
    
