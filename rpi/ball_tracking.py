import numpy as np
import golfConfig as conf
import imutils
from imutils.video import VideoStream
import cv2
import time
# naive implementation of ball detection
# we detect the ball if there is a countour in a range of white values
# and a certain radius

def ball_tracking(frame):
    ball_detected = False
    # the color values that we assume for the golf ball

    # white in hvs color space
    color_upper = (155, 52, 150) # 105, 32, 130
    color_lower = (0, 0, 20)   # 0, 0, 28

    frame = imutils.resize(frame, width = 600)
    # change the color scheme of the frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("color schema", hsv)
    # find the golf ball in the picture
    mask = cv2.inRange(hsv, color_lower, color_upper)
    # remove any noise next to the mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("mask", mask)
    # find the contours of the golf ball and identify the center x,y
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        # find the largest contour
        c = max(cnts, key=cv2.contourArea)
        # compute the min radious of the contour
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # if the contour has a min size proceed
        if radius > 30:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            ball_detected = True
    return ball_detected, frame

if __name__ == '__main__':
    resolution = (400,304)  
    # location = "rpi/vid/2016_10_21 cap1.1.h264"
    camera = cv2.VideoCapture(0)
    camera = VideoStream(src=0, resolution=resolution, framerate=conf.CAMERA_FRAMERATE).start()
    ball_in_picture = False
    while True:
	    # grab the current frame
        (grabbed, frame) = camera.read()
        # frame = camera.read()
        (ball_in_picture, frame_with_marker) = ball_tracking(frame)
        if ball_in_picture:
            print("Ball is in the picture at " + str(time.time()))
        cv2.imshow("Ball", frame_with_marker)
        key = cv2.waitKey(1) & 0xFF

	    # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
