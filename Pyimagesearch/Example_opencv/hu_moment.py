import cv2
# Hu Momentler normalde bir görüntüdeki bir nesnenin siluetinden veya dış hatlarından çıkarılır

image = cv2.imread(r"pyimagesearch\Example_opencv\media\diamond.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # tek kanallı görüntü gerekli

print(cv2.HuMoments(cv2.moments(image)).flatten())

"""
çıktı
[ 6.53608067e-04  6.07480284e-16  9.67218398e-18  1.40311655e-19
 -1.18450102e-37  8.60883492e-28 -1.12639633e-37]
"""