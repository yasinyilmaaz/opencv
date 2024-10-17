import cv2
import matplotlib.pyplot as plt



def sliding_window(image, step, ws):

    for y in range(0, image.shape[0]-ws[1], step): # 0'dan başlayıp resmin yüksekliğinden pencere yüksekliğini çıkartıp adım sayısına kadar git.
        for x in range(0, image.shape[1]-ws[0], step): # 0'dan başlayıp resmin genişliğinden pencere genişliğini çıkartıp adım sayısına kadar git.
            yield (x, y, image[y:y+ws[1], x:x+ws[0]]) # x ve y koordinatları ile pencereyi döndür.

# img = cv2.imread(r"C:\Users\90505\Desktop\model_egitimi\media\husky.jpg")
# im = sliding_window(img, 5 , (200, 150)) 
# # 5 kullanılan adım sayısıdır. 200 ve 150 ise pencerenin boyutlarıdır.

# for i, image in enumerate(im):
#     print(i)
#     if i == 14125:
#         print(image[0], image[1])
#         plt.imshow(image[2])