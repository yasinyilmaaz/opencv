import Solve_More_Advanced_OpenCV.detect_barkod.simple_barcode_detection as simple_barcode_detection
from imutils.video import VideoStream
import argparse
import time
import cv2
# videoda barkot okutma
# tam olarak çalışmıyor

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())


if not args.get("video", False):
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    
else:
     vs = cv2.VideoCapture(args["video"])
     
while True:
    frame = vs.read()
    frame = cv2.flip(frame, 1)
    if frame is None:
        break
    
    box = simple_barcode_detection.detect(frame)
    
    if box is not None:
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
         
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break

if not args.get("video", False):
    vs.stop()
    
else:
    vs.release()
    
cv2.destroyAllWindows()