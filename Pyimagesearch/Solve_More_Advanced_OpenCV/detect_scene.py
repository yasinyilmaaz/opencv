import argparse
import imutils
import cv2
import os

#  video ile denenecek
"""
sahne sınırı ve çekim geçişi algılamayı tartışacağız.

En yaygın sahne sınırı türü "siyaha dönüş "tür.

Adından da anlaşılacağı gibi, bu, bir sahnenin sona erdiği ve videonun siyaha döndüğü,
ardından bir sonraki sahnenin başladığını gösteren şekilde geri döndüğü zamandır.
 
 
ijital bir çizgi romandan kareleri/panelleri otomatik olarak 
ayıklamak gibi gerçek dünyadan bir uygulama aracılığıyla sahne sınırı algılamayı uygulayacağız.
"""

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, type=str, help="path to input video file")
ap.add_argument("-o", "--output",required=True, type=str, help="path to output directory to store frames")
ap.add_argument("-p", "--min-percent", type=float, default=1.0, help="lower boundary of percentage of motion") # Çerçeve hareket yüzdesinin varsayılan alt sınırı.
ap.add_argument("-m", "--max-percent", type=float,default=10.0, help="upper boundary of percentage of motion") # Çerçeve hareket yüzdesinin varsayılan üst sınırı.
ap.add_argument("-w", "--warmup", type=int, default=200, help="# of frames to use to build a reasonable background model") # Arka plan modelimizi oluşturmak için varsayılan kare sayısı.
args = vars(ap.parse_args())

# arka plan çıkarıcı modelimizi başlatır
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

captured = False # karenin yakalanıp yakalanmadığını gösterir
total = 0 # toplam kaç kare yakaladığımızı gösterir
frames = 0 # videomuzdan kaç kare işlediğimizi gösterir


vs = cv2.VideoCapture(args["video"])
(W, H) = (None, None)

while True:
    
    (grabbed, frame) = vs.read()
    
    if frame is None:
        break
    
    orig = frame.copy()
    frame = imutils.resize(frame, width=600)
    mask = fgbg.apply(frame) # arka plan çıkarma işlemi uygulanır
    # Maskedeki beyaz pikseller ön planımızı, siyah pikseller ise arka planımızı temsil eder.
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    if W is None or H is None:
        (H, W) = mask.shape[:2]
        
    
    p = (cv2.countNonZero(mask) / float(W * H)) * 100
    # ön plan piksel yüzdesini, p , "min_percent" sabitiyle karşılaştırır. Eğer p, karenin %N'sinden daha azında hareket olduğunu gösteriyorsa, 
    # bu kareyi yakalamamışsak ve ısınmamız bitmişse, o zaman kaydeder
    if p < args["min_percent"] and not captured and frames > args["warmup"]:
        cv2.imshow("Captured", frame)
        captured = True
        
        filename = "{}.png".format(total) #Dosya adı ve yolunu oluşturur
        path = os.path.sep.join(args["output"],filename)
        total += 1 # Diske yazılan toplam panel sayısını artırın 
        
        print("[INFO] saving {}".format(path))
        cv2.imwrite(path, orig) # Orijinal çerçeveyi diske yazar
    
    elif captured and p >= args["max_percent"]:
        captured = False
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break

    frames += 1

vs.release()
        
        