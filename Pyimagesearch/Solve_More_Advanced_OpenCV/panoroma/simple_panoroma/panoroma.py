# adım 1: İki giriş görüntüsünden anahtar noktaları tespit edin ve yerel değişmez tanımlayıcıları çıkarın.
# adım 2: İki görüntü arasındaki tanımlayıcıları eşleştirin.
# adım 3: Eşleşen özellik vektörlerimizi kullanarak bir homografi matrisi tahmin etmek için RANSAC algoritmasını kullanın.
# adım 4: homografi matrisini kullanarak bir çarpıtma dönüşümü uygulayın.(adım 3teki)
import numpy as np 
import imutils
import cv2

# düzeldi ama daha niye olduğunu anlamadım odsjfkjg 
class Stitcher:
    def __init__(self):
        # opencv sürümünü kontrol eder
        self.isv3 = imutils.is_cv3(or_better=True)
        
    def stitch(self, images, ratio=0.75, reprojThresh=4.0,showMatches=False):
        # Görüntü listesinin sıralaması önemlidir: görüntülerin soldan sağa doğru sıralanmasını beklinir
        (imageB, imageA)= images
        cv2.imshow("imgA",imageB)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # detectAndDescribe: resimlerdeki anahtar noktaları tespit eder
        # yerel değişmez tanımlayıcıları (yani SIFT) çıkarır
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        print("çalışıyor")
        (kpsB, featuresB) = self.detectAndDescribe(imageB)
        
        # matchKeypoints = iki görüntüdeki özellikleri eşleştirmek için kullanılır(aşağıda tanımlandı)
        M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)
        # eğer M == None ise yeterli anahtar nokta bulunamadı demektir. Aynı şekilde geri döndürülür
        if M is None: return None
        (matches, H, status) = M
        # matches =  anahtar nokta eşleşmelerinin bir listesi
        # H = RANSAC algoritmasından türetilen homografi matrisi
        # status = mekansal olarak doğrulandığını gösteren bir indeks listesi 
        
        # warpPerspective = nokta eşleşmelerini görselleştirip görselleştirmeyeceğimizi kontrol eder
        # warpPerspective(çarpıtmak istediğimiz görüntü,  3 x 3 dönüşüm matrisi yani H, çıktı görüntüsünün şekli)
        result = cv2.warpPerspective(imageA, H,(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        if result.shape[0] < imageB.shape[0]:
            # If the height of the result is less than imageB, pad the result
            pad_height = imageB.shape[0] - result.shape[0]
            result = np.pad(result, ((0, pad_height), (0, 0), (0, 0)), 'constant', constant_values=0)
        elif result.shape[0] > imageB.shape[0]:
            # If the height of the result is greater than imageB, pad imageB
            pad_height = result.shape[0] - imageB.shape[0]
            imageB = np.pad(imageB, ((0, pad_height), (0, 0), (0, 0)), 'constant', constant_values=0)
        
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status)
            
            return(result, vis)
        
        return result
    
    
    # bir görüntüyü kabul eder, ardından anahtar noktaları tespit eder ve yerel değişmez tanımlayıcıları çıkarır.
    def detectAndDescribe(self,image):
        # Gauss Farkı (DoG) anahtar nokta dedektörü ve SIFT özellik çıkarıcı kullanılır
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("eeee")
        # opencv sürümünü kontrol ettik
        if self.isv3:
            print("bbb")
            # descriptor = cv2.xfeatures2d.SIFT_create() # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # (kps, features) = descriptor.detectAndCompute(image, None)
            
            
            descriptor = cv2.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(gray, None)
            if kps is None or features is None:
                raise ValueError("Keypoints or features could not be computed.")
            
        else:
            # detector = cv2.FeatureDetector_create("SIFT")
            # kps = detector.detect(gray)
            
            # extractor = cv2.DescriptorExtractor_create("SIFT")
            # (kps, features) = extractor.compute(gray, kps)
            sift = cv2.SIFT_create()
            print(sift)

            
            (kps, features) = sift.detectAndCompute(gray, None)
            print(kps)
        kps = np.float32([kp.pt for kp in kps])
        
        return (kps, features)
    
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reproThresh):
        # her iki görüntüdeki tanımlayıcılar üzerinde döngü yapar,
        # mesafeleri hesaplar ve her tanımlayıcı çifti için en küçük mesafe bulunur
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        
        if featuresA is None or featuresB is None:
            raise ValueError("Features are None")

        if not (isinstance(featuresA, np.ndarray) and isinstance(featuresB, np.ndarray)):
            raise TypeError("Features must be numpy arrays")
        # BruteForce değeri, her iki görüntüdeki tüm özellik vektörleri arasındaki Öklid mesafesini kapsamlı bir
        # şekilde hesaplayacağımızı ve en küçük mesafeye sahip tanımlayıcı çiftlerini bulacağımızı gösterir
        rawMatches = matcher.knnMatch(featuresA,featuresB, k=2)
        # her bir tanımlayıcı çifti için rawMatches'i hesaplar - ancak bu çiftlerden bazılarının
        # yanlış pozitif olma ihtimali vardır, yani görüntü yamaları aslında gerçek eşleşmeler değildir
        matches= []
        
        for m in rawMatches:
            # Yüksek kaliteli özellik eşleşmelerini belirlemek için kullanılan Lowe's oran testini
            # Lowe's oranı için tipik değerler normalde [0,7, 0,8] aralığındadır. Burda 0.75 aldık
            
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        
        if len(matches)> 4:
            
            ptsA = np.float32([kpsA[i] for (_,i) in matches])
            ptsB = np.float32([kpsB[i] for (i,_) in matches])
            
            (H, status) = cv2.findHomography(ptsA,ptsB, cv2.RANSAC, reproThresh)
            
            return (matches, H, status)
        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # Bu değişkenleri kullanarak, ilk görüntüdeki N anahtar noktasından ikinci
        # görüntüdeki M anahtar noktasına düz bir çizgi çizerek "aykırı" anahtar
        # noktalarını görselleştirir
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
        
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            if s ==1:
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
        return vis
            
        