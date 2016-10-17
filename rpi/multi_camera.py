# import the necessary packages
from __future__ import print_function
from motion_detection import BasicMotionDetector
from imutils.video import VideoStream
import golfConfig as conf
import numpy as np
import datetime
import imutils
import time
import cv2

	
def start_record(indicator):
	# define the codec
	fourcc = cv2.VideoWriter_fourcc(*'h264')
	# create openCV Filewriter
	videoWriter = cv2.VideoWriter('output.h264',fourcc, conf.CAMERA_FRAMERATE, conf.CAMERA_RESOLUTION)
	cams[]
	detectors[]
	# number of frames to read
	total = 0
# create video streams and Motion Detectors depending on parameter
	print("[INFO] starting cameras...")
	if indicator == 1:
		picam = VideoStream(usePiCamera=True).start()
		cams = [picam]
		piMotion = BasicMotionDetector()
		detectors = [piMotion]
	elif indicator == 2:
		webcam = VideoStream(src=0).start()
		cams = [webcam]
		webcamMotion = BasicMotionDetector()
		detectors = [webcamMotion]
	elif indicator == 3:
		webcam = VideoStream(src=0).start()
		picam = VideoStream(usePiCamera=True).start()
		cams = [picam, webcam]
		piMotion = BasicMotionDetector()
		webMotion = BasicMotionDetector()
		detectors = [piMotion, webMotion]
		# letting the cameras warm up
	time.sleep(2.0)

# configure the cameras [might want to configure each camera with different parameters]
	for i in range(len(cams)):
		cams[i].resolution = conf.CAMERA_RESOLUTION
		cams[i].framerate = conf.CAMERA_FRAMERATE

	# loop over frames from the video streams
	for filename in conf.CAMERA_FILENAMES:
	# initialize the list of frames that have been processed
		frames = []

	# loop over the frames and their respective motion detectors
	# for (stream, motion) in zip((webcam, picam), (camMotion, piMotion)):
		for (stream, motion) in zip(cams, detectors):
	# read the next frame from the video stream and resize
	# it to have a maximum width of 400 pixels
			frame = stream.read()
			frame = imutils.resize(frame, width=400)

	# convert the frame to grayscale, blur it slightly, update
	# the motion detector
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)
			locs = motion.update(gray)

	# we should allow the motion detector to "run" for a bit
	# and accumulate a set of frames to form a nice average
			if total < 32:
				frames.append(frame)
				continue

	# otherwise, check to see if motion was detected
			if len(locs) > 0:
	# initialize the minimum and maximum (x, y)-coordinates,
	# respectively
				(minX, minY) = (np.inf, np.inf)
				(maxX, maxY) = (-np.inf, -np.inf)

	# loop over the locations of motion and accumulate the
	# minimum and maximum locations of the bounding boxes
				for l in locs:
					(x, y, w, h) = cv2.boundingRect(l)
					(minX, maxX) = (min(minX, x), max(maxX, x + w))
					(minY, maxY) = (min(minY, y), max(maxY, y + h))

	# draw the bounding box
				cv2.rectangle(frame, (minX, minY), (maxX, maxY),
				(0, 0, 255), 3)

	# update the frames list
			frames.append(frame)

	# increment the total number of frames read and grab the 
	# current timestamp
		total += 1
		timestamp = datetime.datetime.now()
		ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")

	# loop over the frames a second time
		for (frame, name) in zip(frames, cams):
	# draw the timestamp on the frame and display it
			cv2.putText(frame, ts, (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
			cv2.imshow(name, frame)

	# check to see if a key was pressed
			key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

	# do a bit of cleanup
	print("[INFO] cleaning up...")
	cv2.destroyAllWindows()
	for i in range(len(cams)):
		cams[i].stop()