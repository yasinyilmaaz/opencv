from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
# örnek çıktı sayısı. varsayılan olarak 21 değerindedir
ap.add_argument("-s", "--sample", type=int, default=21,
	help="# of images to sample")
args = vars(ap.parse_args())
# Verilen görüntüler içersinden rasgele birni seçtik
# images dizini içindeki tüm resim yollarının bir listesini elde etmek için list_images fonksiyonuna bir çağrı yaparız 
imagePaths = list(paths.list_images(args["images"]))
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]


# gelen görüntüleri listeliyoruz
images = []

for imagepath in imagePaths:
    image = cv2.imread(imagepath)
    images.append(image)

# build_montages işlevi üç bağımsız değişken gerektirir
#    image_list : Bu parametre OpenCV aracılığıyla yüklenen görüntülerin bir listesidir.
#    image_shape : Montajdaki her görüntünün genişlik ve yüksekliğini içeren bir tuple.
    #  Burada montajdaki tüm görüntülerin 129 x 196 olarak yeniden boyutlandırılacağını belirtiyoruz.
    #  Montajdaki her görüntüyü sabit bir boyuta yeniden boyutlandırmak,
    #  elde edilen NumPy dizisinde düzgün bir şekilde bellek ayırabilmemiz için bir gerekliliktir.
# montage_shape : İkinci bir tuple, bu montajdaki sütun ve satır sayısını belirtir. 
montages = build_montages(images, (128,196), (7, 3))
# Montajdaki boş alanlar siyah piksellerle doldurulacaktır.


for montage in montages:
    cv2.imshow("Montage", montage)
    cv2.waitKey(0)