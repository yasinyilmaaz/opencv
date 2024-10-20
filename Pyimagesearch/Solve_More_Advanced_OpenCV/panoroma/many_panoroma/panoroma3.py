from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,help="path to the output image")
ap.add_argument("-c", "--crop", type=int, default=0, help="whether to crop out largest rectangular region")
args = vars(ap.parse_args())


imagePaths = sorted(list(paths.list_images(args["images"])))
images = []


for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	images.append(image)


print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

if status == 0:
    
    if args["crop"] > 0:
        print("[INFO] cropping...")
        #  dikilmiş görüntümüzün her tarafına 10 piksellik bir kenarlık ekleniyor
        stitched = cv2.copyMakeBorder(stitched, 10, 10, 10,10, cv2.BORDER_CONSTANT, (0, 0, 0))
        
        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
        cv2.imread("thresh", thresh)
        
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        # yeni dikdörtgen maskemiz için bellek ayırı
        mask= np.zeros(thresh.shape, dtype="uint8")
        # en büyük konturumuzun sınırlayıcı kutusunu hesaplar
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        
        # panoramanın iç kısmına sığana kadar yavaşça küçültülecektir
        minRect = mask.copy()
        # minMask boyutunu küçültmeye devam etmemiz gerekip gerekmediğini belirlemek için kullanılacaktır.
        sub = mask.copy()
        
        # daha fazla ön plan pikseli kalmayana kadar döngüye devam edecek
        while cv2.countNonZero(sub) > 0:
            
            minRect = cv2.erode(minRect, None)
            #  thresh'i minRect'ten çıkarır
            sub = cv2.subtract(minRect, thresh)
            
        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts) # En büyük konturun sınırlayıcı kutusu hesaplandı
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        stitched = stitched[y:y + h, x:x + w] # sınırlayıcı kutuyu kullanarak panoramayı kırptı
        
        cv2.imwrite(args["output"], stitched)
        cv2.imshow("Stitched", stitched)
        cv2.waitKey(0)
    else:
        print("[INFO] image stitching failed ({})".format(status))
    
    