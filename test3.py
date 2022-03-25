import cv2
import time

cap = cv2.VideoCapture("badapple60.mp4")
t = time.time()
count = 0
while (1):
    count = count + 1
    # get a frame
    _, frame = cap.read()
    if frame is None:
        break
print(time.time() - t)
print(count)
