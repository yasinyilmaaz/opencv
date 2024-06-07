from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2



# OpenCV görüntüyü BGR olarak Saklar!!!!!

# Histogram, bir görüntüdeki renklerin dağılımını temsil eder.
# Yoğunluk (piksel değeri) dağılımının üst düzey bir sezgisini veren bir grafik (veya çizim) olarak görselleştirilebilir.
# Bu örnekte bir RGB renk uzayı varsayacağız, dolayısıyla bu piksel değerleri 0 ila 255 aralığında olacaktır.
# Farklı bir renk uzayında çalışıyorsanız, piksel aralığı farklı olabilir.

# Renk histogramlarının "benzerliğini" karşılaştırmak bir mesafe metriği kullanılarak yapılabilir. Yaygın seçenekler şunlardır:
# Öklid, korelasyon, Ki-kare, kesişim ve Bhattacharyya.
# Çoğu durumda, Ki-kare mesafesini kullanma eğilimindeyim, ancak seçim genellikle analiz edilen görüntü veri kümesine bağlıdır

# mask = sıfır değerine sahip piksellerin yok sayıldığı ve sıfırdan büyük bir değere sahip piksellerin histogram hesaplamasına dahil edildiği orijinal görüntümüzle aynı şekle sahip bir uint8 görüntüsüdür.


# Histogramlarımızı oluşturmak için OpenCV'deki cv2.calcHist fonksiyonunu kullanacağız.
# cv2.calcHist(images, channels, mask, histSize, ranges)
# channels = Histogramını hesaplamak istediğimiz kanalın indeksini belirttiğimiz bir indeksler listesi. 
# Mesela gri tonlar için [0]
# mask: Şimdilik, maske için sadece Yok değerini kullanacağız.
# histSize: bir histogram hesaplarken kullanmak istediğimiz kutu sayısıdır. Yine bu, histogram hesapladığımız her kanal için bir tane olmak üzere bir listedir. 
# ranges: Olası piksel değerleri aralığı RGB için [0,256]

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
chans = cv2.split(image)
"""
# gri kanallı resimde histogram çıkarımı

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
hist = cv2.calcHist([gray], [0], None, [256], [0,256]) # histogram hesapladı
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
plt.plot(hist)
plt.xlim([0,256])
plt.show()
"""

"""
çok kanallı resimde histogram çıkarımı

chans = cv2.split(image) # görütüyü kanallarına ayırır (kırmızı, yeşil, mavi)
colors= ("b","g","r")
# PyPlot figürümüzü ayarlıyoruz ve birleştirilmiş histogram listemizi başlatıyoruz
plt.figure()
plt.title("Flattened Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
features = []

for (chan, color) in zip(chans, colors):

    # Şimdi her kanal için bir histogram hesaplanır
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    features.extend(hist)

    # Geçerli kanallar için histogramları çizer
    plt.plot(hist, color= color)
    plt.xlim([0, 256])

print ("flattened feature vector size: %d" % (np.array(features).flatten().shape))
"""
# İki kanalı aynı anda inceleme

fig = plt.figure()

# [83] genellikle çok boyutlu histogramları hesaplarken 8 ila 64 kutucuk arasında bir yer kullanır. Biz 32 kutucuk kullandık

# yeşil ve mavi için 2D renk histogramı çizme
ax = fig.add_subplot(131)
hist = cv2.calcHist([chans[1], chans[0]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation="nearest")
ax.set_title("2D Color Histogram for Green and Blue")
plt.colorbar(p)

# yeşil ve kırmızı için 2D renk histogramı çizme
ax = fig.add_subplot(132)
hist = cv2.calcHist([chans[1], chans[2]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation="nearest")
ax.set_title("2D Color Histogram for Green and Red")
plt.colorbar(p)

# mavi ve kırmızı için 2D renk Histogram Çizme
ax = fig.add_subplot(133)
hist = cv2.calcHist([chans[0], chans[2]], [0,1], None, [32, 32], [0, 256, 0, 256])
p = ax.imshow(hist,interpolation="nearest")
ax.set_title("2D Color Histogram for Blue and Red")
plt.colorbar(p)
print ("2D histogram shape: %s, with %d values" % (hist.shape, hist.flatten().shape[0]))

# 3D histogram işlemi
hist = cv2.calcHist([image],  [0,1,2], None, [8,8,8], [0, 256, 0, 256, 0, 256])
print ("3D histogram shape: %s, with %d values" % (hist.shape, hist.flatten().shape[0]))


plt.show()
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()



"""
Özellik Vektörlerini Kullanarak Bir Görüntünün Nasıl Tanımlanacağını ve Niceliklendirileceğini Açıklıyor*************************



Görüntü Özellik Vektörü: Bir görüntünün içeriğini karakterize etmek ve sayısal olarak ölçmek için kullanılan bir görüntü soyutlaması. 
Normalde gerçek, tamsayı veya ikili değerlidir.
Basitçe ifade etmek gerekirse, bir özellik vektörü bir görüntüyü temsil etmek için kullanılan sayıların bir listesidir.
********************************
Hangi görüntü tanımlayıcısını kullanıyorum? Ham piksel tanımlayıcısı kullanıyorum.
Tanımlayıcımın istisnai çıktısı nedir? Görüntümün ham RGB piksel yoğunluklarına karşılık gelen sayıların bir listesi.
raw = image.flatten()
print(raw)
çıktı = array([255, 255, 255, ..., 255, 255, 255], dtype=uint8)

**************************************
Hangi görüntü tanımlayıcısını kullanıyorum? Bir renk ortalama tanımlayıcısı.
Görüntü tanımlayıcımın beklenen çıktısı nedir? Görüntünün her kanalının ortalama değeri.
means = cv2.mean(image)
# (181.12238527002307, 199.18315040165433, 206.514296508391, 0.0)

************************************
Hangi görüntü tanımlayıcısını kullanıyorum? Bir renk ortalaması ve standart sapma tanımlayıcısı.
Görüntü tanımlayıcımın beklenen çıktısı nedir? Görüntünün her kanalının ortalaması ve standart sapması.
(means, stds) = cv2.meanStdDev(image)
print(means, stds)
# (array([[ 181.12238527],
       [ 199.1831504 ],
       [ 206.51429651]]), array([[ 80.67819854],
       [ 65.41130384],
       [ 77.77899992]]))

       
****************************
Hangi görüntü tanımlayıcısını kullanıyorum? Bir 3D renk histogramı.
Görüntü tanımlayıcımın beklenen çıktısı nedir? Görüntünün renk dağılımını karakterize etmek için kullanılan sayıların bir listesi.
hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
print(hist.shape)
# Özellik vektörü haline getirdik
hist = hist.flatten()
print(hist.shape)

Görüntü tanımlayıcınızın çıktısı bir özellik vektörüdür: 
görüntünüzü karakterize etmek için kullanılan sayıların listesi

"""