from tensorflow.keras.applications.resnet50 import preprocess_input 
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import numpy as np
import cv2
from maximum_non_maximum_pressure import non_maxi_suppression

import os
def file_path_write(file_name):
    file_path = f"media/{file_name}"
    current_directory = os.getcwd() # Bulunduğum dizin
    previous_directory = os.path.dirname(current_directory)# üst dizini
    absolute_path = os.path.join(previous_directory, file_path) #yolları birleştirir
    return absolute_path

import matplotlib.pyplot as plt
def display_image(image, title):
    plt.imshow(image)
    plt.title(title)
    plt.show()

    # selective search
def selective_seaarch(image):
    print("ss")
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(image)
    ss.switchToSelectiveSearchQuality()
    rects = ss.process()

    return rects[:1000]

# model 
model = ResNet50(weights="imagenet")
image = cv2.imread(r"C:\Users\90505\Desktop\model_egitimi\media\animals.jpg")
image = cv2.resize(image, (400, 400))
(H, W) = image.shape[:2]

# ss
rects = selective_seaarch(image)

proposals = []
boxes = []
for (x, y, w, h) in rects:

    if w / float(W) < 0.1 or h / float(H) < 0.1:
        continue

    roi = image[y:y+h, x:x+w]
    roi = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
    roi = cv2.resize(roi, (224, 224))
    roi = img_to_array(roi)
    roi = preprocess_input(roi)
    proposals.append(roi)
    boxes.append((x, y, w, h))

proposals = np.array(proposals)

# predict

print("predict")
preds = model.predict(proposals)
preds = imagenet_utils.decode_predictions(preds, top=1)

labels = {}
min_conf = 0.9

for (i, p) in enumerate(preds):
    (imagenetID, label, prob) = p[0]
    if prob >= min_conf:
        (x, y, w, h) = boxes[i]
        box = (x, y, x+w, y+h)
        L = labels.get(label, [])
        L.append((box, prob))
        labels[label] = L

# non-maximum suppression
clone = image.copy()

for label in labels.keys():
    for (box, prob) in labels[label]:
        boxes = np.array([p[0] for p in labels[label]])
        proba = np.array([p[1] for p in labels[label]])
        boxes = non_maxi_suppression(boxes, proba)
    
        for (startX, startY, endX, endY) in boxes:
            cv2.rectangle(clone, (startX, startY), (endX, endY),(0, 0, 255), 2)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(clone, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
        cv2.imshow("clone", clone)
        if cv2.waitKey(1) & 0xFF == ord('q'):break


