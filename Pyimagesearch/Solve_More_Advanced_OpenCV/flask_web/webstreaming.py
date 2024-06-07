from singlemotiondetector import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

outputFrame = None # bu, istemcilere sunulacak olan kare olacaktır
# uputFrame'i güncellerken iş parçacığı güvenli davranışı sağlamak için kullanılacak bir kilit oluşturuyoruz
# bir iş parçacığının güncellenirken çerçeveyi okumaya çalışmadığından emin oluyoruz
lock = threading.Lock()

# flask uygulamasını başlatıyor
app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/pyimagesearch/Solve_More_Advanced_OpenCV/flask_web/")
def index():
    return render_template("index.html")

def detect_motion(frameCount):
    # frameCount = bg'mizi oluşturmak için gereken minimum kare sayısı 
    global vs, outputFrame, lock
    
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0 #şimdiye kadar okunan toplam kare sayısını
    
    while True:
        frame = vs.read()
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7,7), 0)
        # Daha sonra geçerli zaman damgasını alır ve çerçeveye çizeriz
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I: %M %S %p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
         
        # rka plan çıkarma modelimizi oluşturmak için en az frameCount karesi okuduğumuzdan
        # kontrol ediyoruz
        if total > frameCount:
            # Haraket varsa alıyoruz(konum ve thresh)
            motion = md.detect(gray)
            
            if motion is not None:
                
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY), (0, 0, 255), 2)
                
        md.update(gray) # arka plan modelimizi günceller
        total +=1 # ana kadar kameradan okunan toplam kare sayısını artırır
        
        # iş parçacığı eşzamanlılığını desteklemek için gereken kilidi alır
        with lock:
            outputFrame = frame.copy()

def generate():
    # outputFrame ve lock için global referansları alır
    global outputFrame, lock
    
    # betiği sonlandırana kadar devam edecek sonsuz bir döngü başlatır
    while True:
        
        with lock:
            
            # Gelen görüntünün boş olup olmadığına bakılır
            if outputFrame is None:
                continue
            # ağ üzerindeki yükü azaltmak ve çerçevelerin daha hızlı iletilmesini sağlamak için burada JPEG sıkıştırması gerçekleştirilir
            (flag, encodeImage) = cv2.imencode(".jpg", outputFrame)
            
            if not flag:
                # bu da JPEG sıkıştırmanın başarısız olduğunu ve çerçeveyi yok saymamız gerektiğini gösterir.
                continue
        
        yield (b'--frame\r\n' b'Content-Type:image/jpeg\r\n\r\n' + bytearray(encodeImage) + b'\r\n')
    

@app.route("/video_feed")
def Video_feed():
    # (Kısaca sunucuyu çalıştırır)
    # generate işlevi aracılığıyla bir bayt dizisi olarak kodlanan canlı hareket algılama çıktısıdır.
    # Web tarayıcınız bu bayt dizisini alacak ve tarayıcınızda canlı yayın olarak görüntüleyecek kadar akıllıdır.
    return Response(generate(), mimetype= "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True, help="ip address of the device") # webstream.py dosyasını başlattığınız sistemin IP adresi.
    ap.add_argument("-o", "--port", type=int, required=True, help="ephemeral port number of the server(1024 to 65535)") # Flask uygulamasının çalışacağı port numarası(genellikle 8000 portu kullanılır)
    ap.add_argument("-f","--frame-count", type=int,default=32, help="# of frames used to construct the background mmodel") # areket algılama gerçekleştirilmeden önce arka plan modelini biriktirmek ve oluşturmak için kullanılan kare sayısı
    args = vars(ap.parse_args())
    
    # satırları, hareket algılamayı gerçekleştirmek için kullanılacak bir iş parçacığını başlatır.
    t = threading.Thread(target=detect_motion, args=(args["frame_count"],))
    t.daemon = True
    t.start()
    # Flask uygulamasının kendisini başlatır.
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
    
vs.stop()