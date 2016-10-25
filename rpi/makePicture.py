import cv2
from imutils.video import VideoStream
import time

cam = VideoStream(usePiCamera=True, resolution=(1024, 768)).start()
time.sleep(2)

frame = cam.read()
#print(frame)
cv2.imwrite("frame.png", frame)


cam = VideoStream(src=0, resolution=(1024,768)).start()
time.sleep(2)
frame=cam.read()
cv2.imwrite("frameAction.png", frame)

