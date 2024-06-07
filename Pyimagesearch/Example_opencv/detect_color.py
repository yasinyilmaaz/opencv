import argparse # komut satırı işlemleri için
import numpy as np #sayısal işlemler için
import cv2 # opensv 

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", help="path to the image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])

# renk kodları
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]
# ([17, 15, 100], [50, 56, 200])
# Burada, görüntümüzdeki R >= 100, B >= 15 ve G >= 17 ile birlikte R <= 200, B <= 56 ve G <= 50 olan tüm piksellerin kırmızı olarak kabul edileceğini söylüyoruz.

for (lower, upper) in boundaries:
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # OpenCV kullanarak gerçek renk algılamayı gerçekleştiriyoruz
    # cv2.inRange fonksiyonu üç argüman bekler: birincisi renk tespiti yapacağımız görüntü, ikincisi tespit etmek istediğiniz rengin alt sınırı ve üçüncü argüman tespit etmek istediğiniz rengin üst sınırıdır.
    mask = cv2.inRange(image, lower, upper)
    # Bu satır basitçe cv2.bitwise_and'e bir çağrı yapar ve görüntüde yalnızca maskede karşılık gelen beyaz (255) değere sahip pikselleri gösterir.
    output = cv2.bitwise_and(image, image, mask=mask)

    cv2.imshow("images", np.hstack([image,output]))
    cv2.waitKey(0)


