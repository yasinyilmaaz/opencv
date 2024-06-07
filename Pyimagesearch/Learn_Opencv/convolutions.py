# Konvolüsyonlar
# opencv de bulunan filter2D fonksiyonunu nasıl çalışıyor?

# kernel

# çekirdeği orijinal görüntü boyunca soldan sağa ve yukarıdan aşağıya kaydırıyoruz.
"""
----            ----     ----      ----
|   131  162  232  |    |   131  162  |
|   104  93   139  |    |   104  93   |
|   243  26   252  |     ----      ----
---             ----    

Sol tarafta 3 x 3'lük bir matrisimiz var. Matrisin merkezi açıkça x=1, y=1'de bulunur, burada matrisin sol üst köşesi orijin olarak kullanılır ve koordinatlarımız sıfır indekslidir.
Kerneller tek çekirdek boyutunda olmalıdır
Ancak sağ tarafta 2 x 2'lik bir matrisimiz var. Bu matrisin merkezi x=0.5, y=0.5'te yer alacaktır. Ancak bildiğimiz gibi,
enterpolasyon uygulamadan, piksel konumu (0.5, 0.5) diye bir şey yoktur - piksel koordinatlarımız tam sayı olmalıdır! 
Bu mantık tam olarak tek çekirdek boyutları kullanmamızın nedenidir - çekirdeğin merkezinde her zaman geçerli bir (x, y) koordinatı olmasını sağlamak için.

Konvolüsyonun kendisi aslında çok kolaydır. Tek yapmamız gereken:
Orijinal görüntünün her (x, y) koordinatında durur ve görüntü çekirdeğinin merkezinde bulunan piksellerin komşuluğunu inceleriz.
 Daha sonra bu piksel komşuluğunu alır, bunları çekirdekle konvolüze eder ve tek bir çıktı değeri elde ederiz.
 Bu çıkış değeri daha sonra çıkış görüntüsünde çekirdeğin merkeziyle aynı (x, y) koordinatlarında saklanır.


Orijinal görüntüden bir (x, y) koordinatı seçin.
1.Çekirdeğin merkezini bu (x, y) koordinatına yerleştirin.
2.Giriş görüntü bölgesinin ve çekirdeğin eleman bazında çarpımını alın, ardından bu çarpma işlemlerinin değerlerini tek bir değerde toplayın. Bu çarpımların toplamına çekirdek çıktısı denir.
3.Adım 1'deki aynı (x, y) koordinatlarını kullanın, ancak bu kez çekirdek çıktısını çıktı görüntüsüyle aynı (x, y) konumunda saklayın.
"""

# Konvolüsyon basitçe çekirdek ve çekirdeğin giriş görüntüsünün kapsadığı komşuluk arasındaki eleman-bilge matris çarpımının toplamıdır.


from skimage.exposure import rescale_intensity
import numpy as np
import argparse
import cv2


def convolve(image, kernel):
    # resmin ve kernelin boyutlarını saklıyoruz
    (iH,iW)= image.shape[:2]
    (kH,kW) = kernel.shape[:2]


    pad = (kW -1) // 2
    image = cv2.copyMakeBorder(image, pad,pad,pad,pad,cv2.BORDER_REPLICATE)
    output = np.zeros((iH,iW), dtype="float32")
    # HER SEFERİNDE 1 PİKSEL SOLDAN SAĞA YUKARDAN AŞŞAĞI KAYDIRARAK GÖRÜNTÜ ÜZERİNDE DÖNGÜ YAPAR    
    for y in np.arange(pad, iH + pad):
        for x in np.arange(pad, iW + pad):
            # NumPy dizi dilimleme kullanarak görüntüden İlgi Bölgesini (ROI) çıkarır
            roi = image[y-pad:y+pad + 1, x - pad:x + pad + 1]
            # roi ile kernel elemanlarının çarpımı alınarak ve ardından matristeki girdiler toplanarak gerçekleştirilir
            k = (roi * kernel).sum()
            

            output[y - pad, x - pad] = k
    # Çıktı görüntümüzü [0, 255] aralığına geri getirmek için scikit-image'in rescale_intensity fonksiyonunu uyguluyoruz 
    output = rescale_intensity(output, in_range=(0,255))
    output = (output * 255).astype("uint8")


    return output
        
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="path to input image")
args = vars(ap.parse_args())

smallBlur = np.ones((7,7), dtype="float") * (1 / (7 * 7))
largeBlur = np.ones((21,21), dtype="float") * (1 / (21*21))

sharpe = np.array((
    [0,-1,0],
    [-1,5,-1],
    [0,-1,0]), dtype="int"
    )

laplacian = np.array((
	[0, 1, 0],
	[1, -4, 1],
	[0, 1, 0]), dtype="int")

# construct the Sobel x-axis kernel
sobelX = np.array((
	[-1, 0, 1],
	[-2, 0, 2],
	[-1, 0, 1]), dtype="int")

# construct the Sobel y-axis kernel
sobelY = np.array((
	[-1, -2, -1],
	[0, 0, 0],
	[1, 2, 1]), dtype="int")

kernelBank = (
    ("small_blur", smallBlur),
    ("largeBlur", largeBlur),
    ("sharpe", sharpe),
    ("laplacian", laplacian),
    ("sobelX", sobelX),
    ("sobelY", sobelY),
)

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


for (kernelName, kernel) in kernelBank:
    print("[INFO] applying {} kernel".format(kernelName))
    convoleOutput = convolve(gray,kernel)
    opencvOutput = cv2.filter2D(gray, -1, kernel)


    cv2.imshow("original", gray)
    cv2.imshow("{} - convole".format(kernelName),convoleOutput)
    cv2.imshow("{} - opencv".format(kernelName),opencvOutput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()