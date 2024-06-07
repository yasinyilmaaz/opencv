from imutils import perspective,contours
import numpy as np
import argparse
import imutils
import cv2
from scipy.spatial import distance as dist

# Görüntüdeki nesnelerin boyutunu ölçme


def order_points_old(pts):
    
    """
    Yanlış indeksi seçmek,
    pts listemizden yanlış noktayı seçtiğimiz anlamına gelir. Ve eğer pts'den yanlış noktayı alırsak, saat yönünde üst-sol, üst-sağ, alt-sağ, alt-sol sıralamamız bozulacaktır.
    """
    
    
    # girdi olarak; sol üst, sağ üst, sağ alt ve sol alt sırayla düzenleyeceğimiz noktalar kümesi alır
    
    # koordinat kümemizi saklamak için kullanılacak (4, 2) şeklinde bir NumPy dizisi tanımlıyoruz
    rect = np.zeros((4, 2), dtype="float32")
    
    
    # x ve y değerlerini toplarız, 
    # ardından en küçük ve en büyük toplamları bulunut
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # x ve y değerleri arasındaki farkı alınır
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

# Yukarıda bahsedilen yanlış seçme durumunda 
# oluşaak hatayı çözen yeni halini yazacağız


def order_points(pts):
    # noktaları x değerlerine göre sıralar
    xSorted = pts[np.argsort[:, 0], :]
    
    leftMost = xSorted[:2, :] # en soldaki iki nokta
    rightMost = xSorted[2:, :] # en sağdaki iki nokta
    
    # y eksenindeki noktaları sıralıyor
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    
    # (en üsteki, en alttaki)
    (tl, bl) = leftMost
    
    
    # Sol üst noktayı bir çapa olarak kullanarak Pisagor teoremini uygulayabilir ve sol üst ile en sağ noktalar arasındaki Öklid mesafesini hesaplayabiliriz. Bir üçgenin tanımına göre, hipotenüs dik açılı bir üçgenin en büyük kenarı olacaktır.
    # Böylece, sol üst noktayı çapa olarak aldığımızda, sağ alt nokta en büyük Öklid mesafesine sahip olacak ve sağ alt ve sağ üst noktaları çıkarmamıza izin verecektir 
    D = dist.cdist(tl[np.newaxis], rightMost,"euclidean")[0]
    (br, tr) = rightMost[np.argsort(D)[::-1], :]
    
    return np.array([tl,tr, br, bl], dtype="float32")
    
    
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--new", type=int, default=-1, help="whether or not the new order points should should be used")
args = vars(ap.parse_args())

image = cv2.imread(r"C:\Users\Yasin\Desktop\pyimagesearch\Solve_More_Advanced_OpenCV\media\random.jpeg")
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# soldan sağa doğru sıralarız
cnts = imutils.grab_contours(cnts)

(cnts, _) = contours.sort_contours(cnts)
colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))

for (i, c) in enumerate(cnts):
    if cv2.contourArea(c) < 100:
        continue
    box = cv2.minAreaRect(c)
    box = cv2.boxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        
    print("Object #{}".format(1 +i))
    print(box)
        
    rect = order_points_old(box) # kusurlu order_points
        
    if args["new"] > 0:
            rect = perspective.order_points(box)
            
    print(rect.astype("int"))
    print("")
    
    # Renk listesine göre, sol üst nokta kırmızı, sağ üst nokta mor, sağ alt nokta mavi ve son olarak sol alt nokta deniz mavisi olmalıdır.
    for ((x, y), color) in zip(rect, colors):
        cv2.circle(image, (int(x), int(y)), 5, color, -1)
        
    cv2.putText(image, "Object #{}".format(i + 1), (int(rect[0][0] -15), int(rect[0][1]- 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    