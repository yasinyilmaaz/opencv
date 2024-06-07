import numpy as np
import cv2

# 4 Nokta OpenCV getPerspectiveTransform Örneği

# Bu fonksiyon, dikdörtgenin her bir noktasının (x, y) 
# koordinatlarını belirten dört noktadan oluşan bir liste olan pts adlı tek bir argüman alır.
def order_points(pts):
    # initialzie sıralanacak koordinatların bir listesi
    # listedeki ilk giriş sol üstte olsun,
    # ikinci giriş sağ üst, üçüncü giriş ise
    # sağ alt ve dördüncüsü sol alt
    rect = np.zeros((4, 2), dtype="float32")

    # sol üst nokta en küçük toplama sahip olurken
    # sağ alt nokta en büyük toplama sahip olacaktır
    s = pts.sum(axis= 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # Şimdi, noktalar arasındaki farkı hesaplayın.
    # sağ üst nokta en küçük farka sahip olacaktır,
    # sol alt kısım ise en büyük farka sahip olacaktır
    # np.diff noktalar arası farkı alır (x -y) 
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

# pts listesi, dönüştürmek istediğimiz görüntünün ROI'sini içeren dört noktanın listesidir
# image = görüntü
def four_point_transform(image, pts):
    
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Yeni görüntünün genişliğini belirleriz
    # Burdaki genişlik sağ alt ve sol alt x koordinatları
    # veya sağ üst ve sol üst x koordinatları arasındaki en büyük mesafedir
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # Benzer şekilde burdaki görüntüde de yükseklikleri belirleriz
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] -br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] -bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))


    dst = np.array([
        [0, 0],  # sol üst köşe
        [maxWidth - 1, 0], # sağ üst köşe
        [maxWidth - 1, maxHeight - 1], # sağ alt köşe
        [0, maxHeight - 1] # sol alt köşe
    ], dtype="float32")

    # kuş bakışı görünümünü SAĞLAMAK İÇİN BU FONKSİYONU KULLANACAĞIZ
    # fonksiyona; orijinal görüntüdeki 4 ROI noktasının listesi olan rect ve dönüştürülmüş noktalarımızın listesi veririz
    M = cv2.getPerspectiveTransform(rect, dst)
    # getPerspectiveTransform fonksiyonu, gerçek dönüşüm matrisi olan M 'yi döndürür
    # yukarıdan aşağıya görünümümüz olan çarpıtılmış görüntümüzdür
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped