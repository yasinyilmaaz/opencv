import argparse
import cv2
import imutils
# Resimdeki şekillerin etrafını çizme

ap = argparse.ArgumentParser()
# "-i" = shorthead, "--input" = longhead
ap.add_argument("-i","--input", required=True, help="path to input image")
ap.add_argument("-o","--output", required=True, help="path to output image")
# Namespace olan veriyi dictionaryye çevirir
args = vars(ap.parse_args())

image = cv2.imread(args["input"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    cv2.drawContours(image, [c], -1, (0,0,255),2)

text = f'I found {len(cnts)} total shapes'
cv2.putText(image, text, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)

cv2.imwrite(args["output"], image)



