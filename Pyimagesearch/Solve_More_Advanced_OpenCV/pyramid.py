from helpers import pramid
from skimage.transform import pyramid_gaussian
import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="Path to the image")
ap.add_argument("-s", "--scale", type=float, default=1.5, help="scale factor size")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])


for (i, resized) in enumerate(pramid(image, scale=args["scale"])):
	cv2.imshow("Layer {}".format(i + 1), resized)
	cv2.waitKey(0)
# close all windows
cv2.destroyAllWindows()


for (i, resized) in enumerate(pyramid_gaussian(image,downscale=2)): # her katmanda görüntünün boyutunu yarıya indiriyoruz
    # yeterli minimum boyuta inip inmediği kontrol ediliyor
    if resized.shape[0] < 30 or resized.shape[1] < 30:
        break
    
    cv2.imshow("Layer {}".format(i), resized)
    cv2.waitKey(0)
    

    