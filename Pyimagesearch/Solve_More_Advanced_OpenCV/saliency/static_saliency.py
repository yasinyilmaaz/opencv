# İki algoritma uygular:
# 1. static spectral saliency.
# https://www.sciencedirect.com/science/article/pii/S0262885609001371
# 2. fine grained http://bcmi.sjtu.edu.cn/~zhangliqing/Papers/2007CVPR_Houxiaodi_04270292.pdf

# Spektral çözünürlük, bir sensörün dalga boyu aralıklarını tanımlama yeteneğini tanımlar.

import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])

#  static spectral saliency.

saliency = cv2.saliency.StaticSaliencySpectralResidual_create() # Nesne oluşturuldu
(success, saliencyMap) = saliency.computeSaliency(image) # veri içine aktarıldı
# görüntünün önemli yada ilginç alanları 1 e yakın değerler aldı.
# olmayan alanlarda 0 a yakın değerler aldı 
saliencyMap = (saliencyMap * 255).astype("uint8") # [0, 255] aralığına ölçekleme
cv2.imshow("Image", image)
cv2.imshow("Output", saliencyMap)
cv2.waitKey(0)


# fine grained 

saliency = cv2.saliency.StaticSaliencyFineGrained_create()
(success, saliencyMap) = saliency.computeSaliency(image)
# dönen değerler [0, 255] aralığında ölçeklendirilmiştir

threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]



cv2.imshow("Image", image)
cv2.imshow("Output", saliencyMap)
cv2.imshow("Thresh", threshMap)
cv2.waitKey(0)


