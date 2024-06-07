# Bu algoritma, video akışında hareket eden nesnelerin göze çarpan
# olarak kabul edildiği video akışlarında çalışmak üzere tasarlanmıştır.
#  A fast self-tuning background subtraction algorithm. https://ieeexplore.ieee.org/document/6910012/ 

from imutils.video import VideoStream #  webcam ile çalışalıcağı için
import imutils
import time
import cv2


saliency = None
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    
    frame = vs.read()
    frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=500)
    
    # Wang yöntemini
    if saliency is None:
        saliency = cv2.saliency.MotionSaliencyBinWangApr2014_create()
        saliency.setImagesize(frame.shape[1], frame.shape[0])
        
        saliency.init()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (success, saliencyMap) = saliency.computeSaliency(gray) # sali haritasını hesaplıyorency
    # SaliencyMap [0, 1] aralığında float değerler içerdiğinden, [0, 255] aralığına ölçeklendiririz ve
    # değerin işaretsiz 8 bitlik bir tamsayı olmasını sağlarız
    saliencyMap = (saliencyMap * 255).astype("uint8")
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Map", saliencyMap)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
vs.stop()

        