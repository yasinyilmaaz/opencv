from collections import deque
from threading import Thread
from queue import Queue
import time
import cv2

class KeyClipWriter:
    def __init__(self, bufSize=64, timeout=1.0):
        
        self.bufSize = bufSize # maksimum tutulacak frame sayısı
        self.timeout = timeout # yazılmaya hazır kare yokken uyku zaman aşımı miktarı
        
        self.frames = deque(maxlen=bufSize) # tutulan frameler
        self.Q = None # FIFO yapısı vardır
        self.writer = None #kullanılan cv2.VideoWriter sınıfının bir örneklemesi
        self.thread = None
        self.recording = False # kaydın başlayıp başlamadığını gösterir
        
    def update(self, frame):
        # gelen framleri baştaki indexlere ekliyor
        self.frames.appendleft(frame)
        # Eğer kayıt başladı ise kuyruğu güncelliyor
        if self.recording:
            self.Q.put(frame)
    
    def start (self, outputPath, fourcc, fps):
        self.recording = True # kayıt moduna aldığımızı belirtiyoruz
        self.writer = cv2.VideoWriter(outputPath,fourcc, fps, (self.frames[0].shape[1], self.frames[0].shape[0]), True) # ayarlar ile kayıt başlatılır
        self.Q = Queue() # kuyruk başlatılır
        
        # kareleri videoya yazmak için ayrı bir iş parçacığı oluşturuyoruz - bu şekilde G/Ç işlemlerinin tamamlanmasını bekleyerek ana video işleme hattımızı yavaşlatmıyoruz.
        for i in range(len(self.frames), 0, -1):
            self.Q.put(self.frames[i -1])
            
        self.thread = Thread(target= self.writer, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def write(self):
        #yeni kareleri alacak ve kaydetmeye devam edecek sonsuz bir döngü
        while True:
            # kaydın durdurulup durdurulmayacağını kontrol eder
            if not self.recording:
                return
            
            if not self.Q.empty(): # Q boş değil ise
                frame = self.Q.get() #bir sonraki görüntüyü alır 
                self.writer(frame) # görüntüyü kaydeder kaydeder
                
            else:
                # Q da çerçeve yoksa bekler
                time.sleep(self.timeout)
    # bir video kaydı bittiğinde ve tüm kareleri hemen dosyaya aktarmamız gerektiğinde kullanılır
    def flush(self):
        while not self.Q.empty():
            frame = self.Q.get()
            self.writer.write(frame)
    
    def finish(self):
        self.recording = False # kaydın bittiğini belirtir
        self.thread.join()
        self.flush()# Q da kalan dosyaları aktarır
        self.writer.release()
        