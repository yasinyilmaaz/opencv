import cv2

img = cv2.imread(r"C:\Users\Yasin\Desktop\opencv_2\bird.jpg")

# verinin sürekli gösterilmesini sağlmak için döngü oluşturuldu
while True:
    cv2.imshow("image", img) # veri gösterildi
    
    if cv2.waitKey(1) & 0xFF == 27: # kpatmak için esc basıldı mı diye kontrol ediliyor
        break
    
# cv2.waitKey(0) # yukarda yaptığımız döngü yerine bunuda kullanabiliriz
# görüntünün sürekli ekranda kalmasını sağlıyor 


cv2.destroyAllWindows() #pencerelerin kağnmasını sağlar