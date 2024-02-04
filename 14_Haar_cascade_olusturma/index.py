import cv2
import numpy as np
# 1. Haar Eğitici Yönteminin Belirlenmesi
#   - Serve => üretli
#   - virtual Machine => zahmetli bir yol
#   - Haar Cascade Trainer => kullanacağımız yöntem

# 2. Nesnenib Belirlenmesi
#   Algılanacak nesnenin ne olacağına karar verilmesi

# 3. Veri Kümesi
# Amaçlanan nesne ileilgili pozitif ve negatif resimlerden oluşan bir dosya
#   pozitif resim = algılamak istediğimiz nesnenin bulunduğu
#   negatif resim = algılamak istediğimiz nesnenin bulunmadığı 
#   Toplu resim indirme programı
#   Resim kırpma programı


# İndirdiğimiz resimleri istediğimiz nesnenin olup olmamasına göre ikiye ayırıyoruz
# Bir dosya açıp içine  n ve p adında iki dosya daha oluşturuyoruz
# n dosyasını nesnenin olmadığı görüntüleri
# p dosyasını nesnenin olduğu görüntüleri ekliyoruz


# ****************************************
# Cascade Trainger gui => uygulamanın ismi