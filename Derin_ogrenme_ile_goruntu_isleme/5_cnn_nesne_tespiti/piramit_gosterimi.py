import cv2
import matplotlib.pyplot as plt


def image_premid(image, scale=1.5, minSize=(224, 224)):

    yield image

    while True:

        w = int(image.shape[1] / scale)
        image = cv2.resize(image, (w, w))

        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break

        yield image

# img = cv2.imread(r"C:\Users\90505\Desktop\model_egitimi\media\husky.jpg")
# im = image_premid(img, 1.5, (10, 10))
# for i, image in enumerate(im):
#     plt.figure()
#     plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     plt.title(f"image {i}")
#     plt.show()