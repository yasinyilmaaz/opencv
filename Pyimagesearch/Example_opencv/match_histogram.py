import numpy as np
import cv2
import argparse
from skimage  import exposure
import matplotlib.pyplot as plt
# OpenCV ve scikit-image ile histogram eşleştirme


# Bir giriş görüntüsü yükleyin (yani, "kaynak" görüntü)
# Referans görüntü yükleyin
# Her iki görüntü için histogramları hesaplayın
# Giriş görüntüsünü alıp referans görüntüyle eşleştirerek renk/yoğunluk dağılımını referans görüntüden kaynak görüntüye aktarmak
    
# Histogram eşleştirme en iyi şekilde bir "dönüşüm" olarak düşünülebilir. Amacımız bir giriş görüntüsünü ("kaynak") almak ve piksel yoğunluklarını, giriş görüntüsü histogramının dağılımı bir referans görüntünün dağılımıyla eşleşecek şekilde güncellemektir.

# Giriş görüntüsünün gerçek içeriği değişmese de piksel dağılımı değişir, böylece giriş görüntüsünün aydınlatması ve kontrastı referans görüntünün dağılımına göre ayarlanır.

# import
# pip install opencv-contrib-python
# pip install scikit-image==0.18.1

ap = argparse.ArgumentParser()
ap.add_argument("-s","--source", help="path to do source")
ap.add_argument("-r","--reference", help="path to do reference")
args = vars(ap.parse_args())

print("[INFO] loading source and reference images...")
src = cv2.imread(args["source"])
ref = cv2.imread(args["reference"])

# histogram eşleştirmesi gerçekleştirilir
print("[INFO] performing histogram matching...")
multi = True if src.shape[-1] > 1 else False
matched = exposure.match_histograms(src, ref, channel_axis=-1)

(fig, axs) = plt.subplots(nrows=3, ncols=3, figsize=(8,8))

for (i, image) in enumerate((src,ref,matched)):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for ( j, color) in enumerate(("red","green","blue")):
        (hist, bins) = exposure.histogram(["pyimagesearch\\Example_opencv\\media\\opencv.png",j],source_range="dtype")
        axs[j,i].plot(bins,hist / hist.max())

        (cdf, bins)= exposure.cumulative_distribution(image["pyimagesearch\\Example_opencv\\media\\histogram.png",j])
        axs[j,i].plot(bins, cdf)

        axs[j, 0].set_ylabel(color)

axs[0, 0].set_title("Source")
axs[0, 1].set_title("Reference")
axs[0, 2].set_title("Matched")
# display the output plots
plt.tight_layout()
plt.show()

# show the output images
cv2.imshow("Source", src)
cv2.imshow("Reference", ref)
cv2.imshow("Matched", matched)
cv2.waitKey(0)