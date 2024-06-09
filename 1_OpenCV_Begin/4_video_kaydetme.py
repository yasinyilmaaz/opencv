import cv2
# wepcam körüntü kaydetme

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

fileName= "D:\wepcam.avi"
codec= cv2.VideoWriter_fourcc("W","M","V","2") 
frameRate= 30 # 30 frame/saniye
resolution = (640,480)
videoFileOutput =cv2.VideoWriter(fileName,codec,frameRate,resolution) # VideoWriter nesnesi oluşturuldu                                                                                                                                                                                                                                                                                                                  

while True:
    ret, frame = cap.read()
    if ret == 0: #gösterilecek frame kalmadıysa döngüden çıkar
        break
    frame = cv2.flip(frame,1) # aynalama işlemi
    videoFileOutput.write(frame) # video dosyasına yazma işlemi
    cv2.imshow("Webcam new", frame) # webcam görüntüsünü gösterir

    if cv2.waitKey(1) % 0xFF == ord("q"): # q tuşuna basıldığında döngüden çıkar
        break

videoFileOutput.release() # video dosyasını kapatır
cap.release() # webcam kapatılır
cv2.destroyAllWindows()

