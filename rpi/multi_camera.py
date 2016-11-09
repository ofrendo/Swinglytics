# import the necessary packages
from __future__ import print_function
from motion_detection import BasicMotionDetector
from imutils.video import VideoStream
import subprocess as sp
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

def start_md(indicator, triggerMotion, cameraFilenames, cameraFilenameTS):
	FFMPEG_BIN = 'ffmpeg'
	cams = []
	detectors = []
	# define the codec: see http://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/ for combinations
	#fourcc = cv2.VideoWriter_fourcc(*'XVID') # DOES NOT WORK WITH .avi
	#print("XVID", fourcc)
	# fourcc = cv2.VideoWriter_fourcc(*'MJPG') # THIS ONE WORKS WITH .avi
	#print("MJPG", fourcc)
	#fourcc = cv2.VideoWriter_fourcc(*'h264')
	#fourcc = cv2.VideoWriter_fourcc(*'H264') # DOES NOT WORK with .avi, NOR .mkv (even though it takes longer)
	#fourcc = cv2.VideoWriter_fourcc(*'X264') # DOES NOT WORK with .avi, .wmv, mp4
	#fourcc = cv2.VideoWriter_fourcc(*'mp4v') # DOES NOT WORK WITH .mp4
	
	#fourcc = cv2.VideoWriter_fourcc('A','B','E','F')
	#print("third", fourcc)

	# create video streams and Motion Detectors depending on parameter
	print("########################### CAMERA ##############################")
	print("Starting motion detection camera=", indicator, " recording at", conf.CAMERA_RESOLUTION[0], "x", conf.CAMERA_RESOLUTION[1], "with", conf.CAMERA_FRAMERATE, "fps...")
	print("##################################################################")
	fps = conf.CAMERA_FRAMERATE
	cam = None
	resolution = (640,480)
	if indicator == 1:
		cam = VideoStream(usePiCamera=True, resolution=resolution, framerate=fps).start()
							#, resolution=conf.CAMERA_RESOLUTION
	elif indicator == 2:
		cam = VideoStream(src=0, resolution=resolution, framerate=fps).start()
	fourcc = cv2.VideoWriter_fourcc(*'x264')
	writer = None
	(h, w) = (None, None)
	zeros = None
	detector = BasicMotionDetector()
	#cam.resolution = (640,480) #conf.CAMERA_RESOLUTION
	#cam.framerate = conf.CAMERA_FRAMERATE
	frames = []
	# letting the cameras warm up
	time.sleep(2.0)
	#print(cam)

	# number of frames to read
	total = 0

	for filename in itertools.cycle(cameraFilenames): #in ["temp.h264"]:
		command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '1024x768', # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '24', # frames per second
        '-i', '-', # The imput comes from a pipe
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'mpeg',
        '/rpi/vid/my_output_videofile.mp4' ]

		pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)
		
		# create openCV Filewriter: one per file (4 circular files)
		# save when this file was written to
		#i = getFileIndex(filename, cameraFilenames)
		#cameraFilenameTS[i] = time.time()

		#videoWriter = cv2.VideoWriter(filename, fourcc, conf.CAMERA_FRAMERATE, conf.CAMERA_RESOLUTION, True) # conf.CAMERA_RESOLUTION
		#videoWriter = cv2.VideoWriter("test.avi", fourcc, conf.CAMERA_FRAMERATE, (680,480))
		#print("[CAMERA", indicator, "] Recording to",  filename, "at", cameraFilenameTS[i])

		# loop over the frames 
		frameCounter = 0
		while(frameCounter < conf.CAMERA_CAP_LEN_FRAMES): # e.g. 150
			
			# read the next frame from the video stream and resize
			# it to have a maximum width of 400 pixels
			frameCounter += 1
			total += 1

			frame = cam.read()
			frame = imutils.resize(frame, width = 300)
			#cv2.imshow("Golf", frame)
			startTime = time.time()
			#frameGray = imutils.resize(frame, width=400)
			#print(frame)
			# convert the frame to grayscale, blur it slightly, update
			# the motion detector
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)
			locs = detector.update(gray)
			
			# we should allow the motion detector to "run" for a bit
			# and accumulate a set of frames to form a nice average
			# also reset frames so that the video is only cut when we have the average
			if total < 32:
				#frameCounter = 0
				#frames.append(frame)
				continue

			# otherwise, check to see if motion was detected
			if len(locs) > 0:
				ts = time.time()
				print("Motion detected at", ts, "with camera=", indicator)
				triggerMotion.value = ts

				
				#rectangle detection
					# initialize the minimum and maximum (x, y)-coordinates,
				# 	# respectively
				(minX, minY) = (np.inf, np.inf)
				(maxX, maxY) = (-np.inf, -np.inf)

				# 	# loop over the locations of motion and accumulate the
				# 	# minimum and maximum locations of the bounding boxes
				for l in locs:
					(x, y, w, h) = cv2.boundingRect(l)
					(minX, maxX) = (min(minX, x), max(maxX, x + w))
					(minY, maxY) = (min(minY, y), max(maxY, y + h))

				grayOnlyChanges = cv2.absdiff(gray, cv2.convertScaleAbs(detector.avg)) 
				timeChanged = time.time()
				cv2.imwrite("rpi/vid/img/frameBlurredOnlyChanges" + str(int(time.time())) + ".png", grayOnlyChanges)

				# # draw the bounding box
				cv2.rectangle(gray, (minX, minY), (maxX, maxY),
				(0, 0, 255), 3)
				
				
				cv2.rectangle(frame , (minX, minY), (maxX, maxY),
				(0, 255, 0), 3)
				cv2.imshow("movement", frame)
				cv2.imwrite("rpi/vid/img/frame" + str(int(time.time())) +  ".png", frame)
				cv2.imwrite("rpi/vid/img/frameBlurred" + str(int(time.time()))  + ".png", gray)
			cv2.rectangle(frame , (75, 25), (225,200), (0, 0, 255), 3)
			cv2.imshow("boundary", frame)
			#frames.append(frame)
			# loop over the frames a second time
			#startTime = time.time()			
			#videoWriter.write(frame)
			#print("Writing took", (time.time() - startTime), "it should take", (1/conf.CAMERA_FRAMERATE))
			
			#print("Frame processing took", (time.time() - startTime), "it should take", (1/conf.CAMERA_FRAMERATE))

				# if total > 32:
				# 	print("total > 32")
					# for (frame, name) in zip(frames, [cam]):
					# 	print("writing frame")
					# 	videoWriter.write(frame)
			if writer is None:
				(h, w) = frame.shape[:2]
				# writer = cv2.VideoWriter('rpi/vid/mc_vid.avi', fourcc, fps, (w, h), True)
				writer = cv2.VideoWriter(filename, fourcc, fps, (w, h), True)
				zeros = np.zeros((h, w), dtype='uint8')		
			
			# write the output frame to file
			writer.write(frame)
		
		# draw the timestamp on the frame and display it
		# cv2.putText(frame, ts, (10, frame.shape[0] - 10),
		# cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		# cv2.imshow(name, frame)
			# cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
			
				# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

	# do a bit of cleanup
	print("[INFO] cleaning up...")
	cv2.destroyAllWindows()
	cam.stop()
	writer.release()

# Only executed if explicitely calling this file: use for testing purposes
if __name__ == '__main__':
	if len(sys.argv)>1 and int(sys.argv[1]) == 2:
		start_md(2, conf.CAMERA_TRIGGER_MOTION2, 
					conf.CAMERA_FILENAMES2,
					conf.CAMERA_FILENAMES_TS2) 
	else:
		start_md(1, conf.CAMERA_TRIGGER_MOTION1, 
					conf.CAMERA_FILENAMES1,
					conf.CAMERA_FILENAMES_TS1) 


	
