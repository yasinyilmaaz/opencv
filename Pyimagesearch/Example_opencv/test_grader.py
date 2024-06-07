from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# Kabarcık sayfası tarayıcısı ve derecelendiricisi

# Optik İşaret Tanıma'nın (OMR)
# Optik İşaret Tanıma veya kısaca OMR,
# insan tarafından işaretlenmiş belgeleri otomatik olarak analiz etme ve
# sonuçlarını yorumlama işlemidir.


# Kabarcık sayfası tarayıcısı ve derecelendiricisi oluşturmak için 7 adım
# 1. adım: görüntüdeki sınavı tespit etme
# 2. adım: yukarıdan aşağıya, kuş bakışı görünümünü çıkarmak için bir perspektif dönüşümü uygulayın.
# 3. adım: olası cevap seçeneklerini perspektife dönüştürülmüş sınavdan çıkarın.
# 4. adım: Soruları/kabarcıkları satırlar halinde sıralayın.
# 5. adım: Her satır için işaretli yanıtı belirleyin.
# 6. adım: Kullanıcının seçiminde doğru olup olmadığını belirlemek için cevap anahtarımızda doğru cevabı arayın.
# 7. adım: Sınavdaki tüm sorular için tekrarlayın.

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# soruların cevap anahtarını tanımlayın
ANSWER_KEY = {0 : 1, 1 : 4, 2: 0, 3: 3, 4: 1}

# Yumuşatma yaparak kenarları algılıyoruz
# Kenarların belirgin olması perspektif için önemlidir
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

# en az bir kontur olduğunu bakılır
if len(cnts) > 0:
    # azalan sıra ile konturları boyutlarına göre sıralayın.
    cnts = sorted(cnts, key= cv2.contourArea, reverse=True)

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            docCnt = approx
            break

# kuş bakışı görünümünü elde etmek için bir perspektif dönüşümü uygulanabilir
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

# Görüntüyü derecelendirme

thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV| cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts= imutils.grab_contours(cnts)
cnts = sorted(cnts, key= cv2.contourArea, reverse=True)
# teste işaretlenen yerleri tutar
questionCnts = []

for c in cnts:

    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    
    # Bir kontur alanının kabarcık olarak kabul edilebilmesi için bölgenin

    # Yeterince geniş ve uzun olmalıdır (bu durumda her iki boyutta da en az 20 piksel olmalıdır).
    # En boy oranının yaklaşık olarak 1'e eşit olması.
    # Bu kontroller geçerli olduğu sürece questionCnts listemizi güncelleyebilir ve bölgeyi bir baloncuk olarak işaretleyebiliriz.


    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
        questionCnts.append(c)



# OMR sistemimizin "notlandırma" 
# soru konturlarını yukarıdan aşağıya doğru sıralayın
questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
correct = 0

for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
    # Her sorunun 5 olası yanıtı olduğundan, mevcut kontur 
    # kümesini soldan sağa sıralamak için NumPy dizi dilimleme ve kontur sıralama uygulayacağız.
    cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
    bubled = None
    
    # sıralanmış konturlar üzerinde döngü
    for (j, c) in enumerate(cnts):

        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask) # içindeki sıfır olmayan piksel sayısı sayılır
        # Ne kadar çok sıfır olmayan piksel sayarsak, o kadar çok ön plan pikseli vardır
        # sıfır sayısı az olan alanişaretlenen baloncuktur
        if bubled is None or total > bubled[0]:
            bubled = (total, j)

            color = (0, 0, 255) # kırmızı renk
            k = ANSWER_KEY[q] # doğru cevap alınır

            # doğru olup olmadığı kontrol edilir
            if k == bubled[1]:
                color = (0, 255, 0) # yeşil renk
                correct += 1
                print(correct)
        
        cv2.drawContours(paper, [cnts[k]], -1, color, 3)
print(correct)
score = (correct / 5) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Daire algılayarak yapılamaz mıydı?
# eğer öyle yapsaydık dairenin dışına taşma durumları algılayamayabilirdi
# Hough daireleri dış hatlarındaki deformasyonlarla pek iyi başa çıkamaz bu durumda daire algılamanız tamamen başarısız olur.

# iyileştirme
# aynı satırda iki şık işaretlemeyi engelleme
# eğer satırda işaretli kutucuk yok ise atlandı diye işaretlenebilir
# 