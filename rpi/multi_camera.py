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
import sys
import itertools



def getFileIndex(filename, filenames):
    for i in range(len(filenames)):
        if filename == filenames[i]:
            return i

def start_record(indicator, triggerMotion, cameraFilenames, cameraFilenameTS):
	cams = []
	detectors = []
	# define the codec
	fourcc = cv2.VideoWriter_fourcc(*'h264')
	
	# create video streams and Motion Detectors depending on parameter
	print("[INFO] starting cameras with camera=", indicator, "...")
	cam = None
	if indicator == 1:
		cam = VideoStream(usePiCamera=True).start()
	elif indicator == 2:
		cam = VideoStream(src=0).start()

	detector = BasicMotionDetector()
	cam.resolution = conf.CAMERA_RESOLUTION
	cam.framerate = conf.CAMERA_FRAMERATE
	frames = []
	# letting the cameras warm up
	time.sleep(1.0)

	# number of frames to read
	total = 0

	for filename in itertools.cycle(cameraFilenames):
		# create openCV Filewriter: one per file (4 circular files)

		# save when this file was written to
		i = getFileIndex(filename, cameraFilenames)
		cameraFilenameTS[i] = time.time()
	
		videoWriter = cv2.VideoWriter(filename, fourcc, conf.CAMERA_FRAMERATE, conf.CAMERA_RESOLUTION, False)
		# loop over the frames 
		frameCounter = 0;
		while(frameCounter < conf.CAMERA_CAP_LEN_FRAMES): # e.g. 150
			
			stream = cam
			motion = detector

			# read the next frame from the video stream and resize
			# it to have a maximum width of 400 pixels
			frameCounter += 1
			total += 1

			frame = stream.read()
			frameGray = imutils.resize(frame, width=400)

			# convert the frame to grayscale, blur it slightly, update
			# the motion detector
			gray = cv2.cvtColor(frameGray, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)
			locs = motion.update(gray)

			# we should allow the motion detector to "run" for a bit
			# and accumulate a set of frames to form a nice average
			# also reset frames so that the video is only cut when we have the average
			if total < 32:
				frameCounter = 0
				frames.append(frame)
				continue

			# otherwise, check to see if motion was detected
			if len(locs) > 0:
				ts = time.time()
				print("Motion detected at", ts, "with camera=", indicator)
				triggerMotion.value = ts
				
				# rectangle detection
				# 	# initialize the minimum and maximum (x, y)-coordinates,
				# 	# respectively
				# 				(minX, minY) = (np.inf, np.inf)
				# 				(maxX, maxY) = (-np.inf, -np.inf)

				# 	# loop over the locations of motion and accumulate the
				# 	# minimum and maximum locations of the bounding boxes
				# 				for l in locs:
				# 					(x, y, w, h) = cv2.boundingRect(l)
				# 					(minX, maxX) = (min(minX, x), max(maxX, x + w))
				# 					(minY, maxY) = (min(minY, y), max(maxY, y + h))

				# # draw the bounding box
				# 				cv2.rectangle(frame, (minX, minY), (maxX, maxY),
				# 				(0, 0, 255), 3)

			# loop over the frames a second time
			#if total > 32:
			#	for (frame, name) in zip(frames, cams):
			
			videoWriter.write(frame)
			# draw the timestamp on the frame and display it
			# cv2.putText(frame, ts, (10, frame.shape[0] - 10),
			# cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
			# cv2.imshow(name, frame)



	# do a bit of cleanup
	print("[INFO] cleaning up...")
	cv2.destroyAllWindows()
	cam.stop()


if __name__ == '__main__':
    # Only executed if explicitely calling this file: use for testing purposes
    start_record(int(sys.argv[1]), conf.CAMERA_TRIGGER_MOTION1, 
    				conf.CAMERA_FILENAMES1,
    				conf.CAMERA_FILENAMES_TS1) 
