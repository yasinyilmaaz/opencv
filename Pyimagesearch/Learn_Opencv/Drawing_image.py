import cv2
import imutils

image = cv2.imread("pyimagesearch/Learn_Opencv/media/jp.jpg")

output = image.copy()
cv2.rectangle(output, (320, 60), (420, 180), (0,0,255), 2)
cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
# (img, text, başlangıç konumu, font, font boyutu, renk, kalınlık)
cv2.putText(output, "OpenCV + Jurassic Park!!!", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow("Rectangle", output)
cv2.imshow("img", image)
cv2.waitKey(0)