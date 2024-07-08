import cv2
import numpy as np
import argparse
from imutils import paths

# Görüntüler mission4 klasörün içinde

ap = argparse.ArgumentParser()
ap.add_argument("-i","--images", type=str, required=True,help="path to input directory of images to stitc")
args = vars(ap.parse_args())

imagePaths = sorted(list(paths.list_images(args["images"]))) # Görüntüleri yükler ve sıralar

images = []
# magePath için görüntüyü yükler ve görüntüler listesine ekleriz
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)
    
throw = 0
for u in range(1, len(images)):
    img1 = images[u-1]
    img2 = images[u]
    
    img1 = cv2.resize(img1, (500, 500))
    img2 = cv2.resize(img2, (500, 500))
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Her iki yöntemde çalışır
    diff = cv2.absdiff(gray1, gray2) 
    bitwise_xor = cv2.bitwise_xor(gray1, gray2)
    
    _, diff_thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(diff_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for a,contour in enumerate(contours):
        # Atışı kare içine alma
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Atışın merkezine olan mesafeyi hesapla
        distance = np.sqrt((x - 250)**2 + (y - 250)**2)
        
        data = 35
        throw += 1
        # atışın merkezine olan mesafeye göre puanlama yap
        for i in range(1,7):
            if 6 != i:
                if distance < data:
                    print(f"{throw}. atışta {i} puan alındı")
                    break
            else:
                print(f"{throw}. Atış alan dışı")
                break
            data += 50
            
    cv2.imshow('Contours', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
