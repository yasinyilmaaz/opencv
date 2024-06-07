import cv2

# Kare =videonun herhangi bir anındaki resim
# video = Birçok karenin bir araya gelmesidir

# video okuma işlemi
# eğer wepcam kullanmak için 0 yazarız
#  eğer kayıtlı bir video kullanacaksak adresini kullanırız
# cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture("antalya.mp4")


# videoların karaleriniokuyarak tek tek göstereceğiz
# direk video okumak diye şuanlık birşey yok!!!!

while True:
    # iki değer döndürür 
    # ilk değer doğru okuduysa True
    # ikinci değer kareleri döndürür
    ret, frame = cap.read() # framede kareler ters gelir
    # gösterilecek kare olmayınca döngüyü durduruldu
    if ret == 0:
        break

    frame = cv2.flip(frame,1) # aldığımız görüntüyü istediğimiz eksenlere göre çevirir
    cv2.imshow("wepcam0",frame)
    if cv2.waitKey(50) & 0XFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()