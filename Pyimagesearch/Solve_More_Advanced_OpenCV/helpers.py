import imutils
from skimage.transform import pyramid_gaussian

# Orantılı büyütmenin mantığı

def pramid(image, scale=1.5, minSize=(30, 30)):
    # scale = her katmanda ne kadar yeniden boyutlanacağı
    # minSize = bir görüntünün minimum genişlik ve yüksekliği
    yield image
    
    while True:
        
        w = int(image.shape[1] / scale) # yeni görüntünün boyutu hesaplanır
        image = imutils.resize(image, width=w) # en boy oranı kontrol edilir
        
        # görüntünün minimum boyutları karşıladığı kontrol edilir
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        
        
        yield image
        
