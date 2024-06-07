from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

# Video kydetme

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="path to output video file") # video
ap.add_argument("-p","--Picamera", type=int,default=-1, help="wheter or not the Raspberry pi camera shoeld be") # hangi video yada kamera ile mi kaydedilecek
ap.add_argument("-f","--fps", type=int, default=15, help="FPS of output video") # videonun fps değeri
ap.add_argument("-c","--codec", type=str, default="MJPG", help="codec of output video") # sıkıştırma formatı ve renk/piksel formatı için bir tanımlayıcı olan FourCC'yi veya dört karakterli kodu
args = vars(ap.parse_args())

print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["Picamera"]>0)
time.sleep(2.0)

fourcc = cv2.VideoWriter_fourcc(*args["codec"])
writer = None
(h, w) = (None, None)
zeros = None

while True: 
    frame = vs.read()
    frame = imutils.resize(frame, width=300)
    
    if writer is None:
        (h, w) = frame.shape[:2]
        writer = cv2.VideoWriter(args["output"], fourcc, args["fps"], (w * 2, h * 2), True)
        zeros = np.zeros((h, w), dtype="uint8")
        # alınan framedeki rgb değerlerini ayırdık
        (B, G, R) = cv2.split(frame)
        R = cv2.merge([zeros, zeros, R])
        G = cv2.merge([zeros, G, zeros])
        B = cv2.merge([B, zeros, zeros])
        
        # Aldığımız tonlrda resmi tekrar gösterdik
        output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
        output[0:h, 0:w] = frame # orjinal sol üst köşe
        output[0:h, w:w*2] = R # kırmızı sağ üst köşe
        output[h:h*2,w:w*2] = G # yeşil sol alt köşe
        output[h:h * 2,0:w] = B # mavi sağ alt köşe
        
        writer.write(output)
        
        cv2.imshow("Frame", frame)
        cv2.imshow("Output", output)
        key = cv2.waitKey(1) & 0xFF
        
        
        if key == ord("q"):
            break
        
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
writer.release()
        
    

