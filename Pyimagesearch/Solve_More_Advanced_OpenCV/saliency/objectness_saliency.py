# Nesne öneri bölgelerinin bir listesini oluşturmak için BING Objectness Saliency yöntemini kullanır
# BING belirginlik dedektörü çeşitli pencere boyutları, renk uzayları ve matematiksel işlemler için dokuz ayrı model dosyası gerektirir.

import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to BING objectness saliency model")
ap.add_argument("-i", "-image", required=True, help="path to input image")
ap.add_argument("-n", "--max-detections", type=int, default=10, help="maximum # of detections to examine") #  maksimum tespit sayısı
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

saliency = cv2.saliency.ObjectnessBING_create()
saliency.setTrainingPath(args["model"])
(success, saliencyMap) = saliency.computeSaliency(image)
mumDetections = saliencyMap.shpe[0]

# maksimum tespit sayısına kadar tespitler üzerinde döngü oluşturur
for i in range(0, min(mumDetections,args["max_detections"])):
    (startX, startY, endX, endY) = saliencyMap[i].flatten() # sınırlayıcı kordinatlar
    output= image.copy()
    color = np.random.randint(0,255, size=(3,)) # random renk ataması
    color = [int(c) for c in color]
    cv2.rectangle(output, (startX, startY), (endX, endY), color, 2)
    
    cv2.imshow("Image", output)
    cv2.waitKey(0)
