
import multiprocessing as mp
import time
import sys
import subprocess
import struct

import cv2
from camera import start_record
from multi_camera import start_md
from soundListenerUSB import start_listening, start_recording
import golfConfig as conf
import handlerCloudStorage as storage

clipStartToMiddleDuration = 2.5
clipMiddleToEndDuration = 2.5
lastSwingRecorded = -1


def printSwingConsoleMessage():
	print("  ____          _                                          _          _ _ ")
	print(" / ___|_      _(_)_ __   __ _   _ __ ___  ___ ___  _ __ __| | ___  __| | |")
	print(" \___ \ \ /\ / / | '_ \ / _` | | '__/ _ \/ __/ _ \| '__/ _` |/ _ \/ _` | |")
	print("  ___) \ V  V /| | | | | (_| | | | |  __/ (_| (_) | | | (_| |  __/ (_| |_|")
	print(" |____/ \_/\_/ |_|_| |_|\__, | |_|  \___|\___\___/|_|  \__,_|\___|\__,_(_)")
	print("                        |___/                                             ")



def createSwingClip(tsMiddle, cameraFilenameTS):
	printSwingConsoleMessage()

	# need to find appropriate file(s) to cut from with the help of tsMiddle
	# for this use the shared array which saves when each file was started to be written
	print("[HANDLER] Swing ts:", tsMiddle)

	# first check file that part of the clip must be in
	# this file can either contain the complete clip (1), the first part (2) or the second part (3)
	# (1) |--------+++++-cap1--------------|-------------cap2--------------|
	#                ^
	# (2) |--------------cap1-----------+++|++-----------cap2--------------|
	#                                     ^ 
	# (3) |--------------cap1-------------+|++++---------cap2--------------|
	#                                        ^     

	# First find the file
	filename0 = "" # is the previous file
	filename1 = "" # is the file tsMiddle is located in
	filename2 = "" # is the next file
	diffToFirstClipStart = -1

	# Correct tsMiddle by a small amount because sound faster than the camera
	tsMiddle += 0
	for i in range(len(cameraFilenameTS)): 
		diffToFirstClipStart = tsMiddle - cameraFilenameTS[i]
		if diffToFirstClipStart <= conf.CAMERA_CAP_LEN:
			filename0 = conf.CAMERA_FILENAMES1[(i-1) % len(conf.CAMERA_FILENAMES1)]
			filename1 = conf.CAMERA_FILENAMES1[i]
			filename2 = conf.CAMERA_FILENAMES1[(i+1) % len(conf.CAMERA_FILENAMES1)]
			# soundname0 = conf.AUDIO_FILENAMES[(i-1) % len(conf.AUDIO_FILENAMES)]
			# soundname1 =  conf.AUDIO_FILENAMES[i]
			# soundname2 =  conf.AUDIO_FILENAMES[(i+1) % len(conf.AUDIO_FILENAMES)]
			break


	# Next check which case we are in
	print("[HANDLER] Handler is sleeping (waiting for files to finish writing)...")
	case = -1
	if diffToFirstClipStart >= clipStartToMiddleDuration:
		# Either (1) or (2)
		if conf.CAMERA_CAP_LEN - diffToFirstClipStart >= clipMiddleToEndDuration:
			# (1) ==> this file is sufficient 
			# still need to wait for this cap to finish writing however
			print("[HANDLER] CASE1: no concat necessary: Using", filename1)
			case = 1
			time.sleep(conf.CAMERA_CAP_LEN)
		else:
			# (2) ==> must retrieve something from the following clip
			print("[HANDLER] CASE2: retrieve something from following clip: Using", filename1, "and", filename2)
			case = 2
			time.sleep(clipStartToMiddleDuration + conf.CAMERA_CAP_LEN)
	else:
		# (3) ==> we must retrieve something from the previous clip
			print("[HANDLER] CASE3: retrieve something from previous clip: Using", filename0, "and", filename1)
			case = 3
			time.sleep(conf.CAMERA_CAP_LEN)
	

	# All neccessary files are now assumed to have been finished
	# Use ffmpeg to cut and concat

	# First need to convert to mp4 ("mux" or "creating a container"): rpi stores it as "raw" h264
	# (http://stackoverflow.com/questions/38112711/how-to-get-the-duration-bitrate-of-a-h264-file-with-avconv-ffmpeg)
	if case == 1:
		convertToMP4(filename1)
		# combineMP4withWAV(filename1, soundname1)
		cutMP4(filename1, 
			diffToFirstClipStart-clipStartToMiddleDuration, 
			clipStartToMiddleDuration+clipMiddleToEndDuration,
			"rpi/vid/swingClip.mp4")
	elif case == 2:
		convertToMP4(filename1)
		# combineMP4withWAV(filename1, soundname1)
		convertToMP4(filename2)
		# combineMP4withWAV(filename2, soundname2)
		cutMP4(filename1, diffToFirstClipStart-clipStartToMiddleDuration, None, "rpi/vid/swingClipP1.mp4")
		cutMP4(filename2, 0, clipMiddleToEndDuration - (conf.CAMERA_CAP_LEN-diffToFirstClipStart), "rpi/vid/swingClipP2.mp4")
		concatenateMP4("rpi/vid/swingClipP1.mp4", "rpi/vid/swingClipP2.mp4")
	elif case == 3:
		convertToMP4(filename0)
		# combineMP4withWAV(filename0, soundname0)
		convertToMP4(filename1)
		# combineMP4withWAV(filename1, soundname1)
		cutMP4(filename0, conf.CAMERA_CAP_LEN- (clipStartToMiddleDuration-diffToFirstClipStart), None, "rpi/vid/swingClipP1.mp4")
		cutMP4(filename1, 0, diffToFirstClipStart + clipMiddleToEndDuration, "rpi/vid/swingClipP2.mp4")
		concatenateMP4("rpi/vid/swingClipP1.mp4", "rpi/vid/swingClipP2.mp4")
	# p.wait #sync

	createThumbnail("rpi/vid/swingClip.mp4")
	# Upload files in new subprocesses
	processUploadVideo = mp.Process(name="processUploadVideo",
									target=storage.uploadFile,
									args=("rpi/vid/swingClip.mp4",
										"rpi/vid/swingClip.png", 
									 		 tsMiddle))
	processUploadVideo.daemon = True
	processUploadVideo.start()

	print("[HANDLER] Handler is listening...")

def convertToMP4(filename):
	print("[HANDLER]  Converting", filename, "to mp4...")
	# -y overwrite without asking
	# -r define framerate: otherwise ffmpeg will use default 25fps
	# -i input file
	# -c copy 
	# output file
	subprocess.call(["ffmpeg -loglevel quiet -y -r " + str(conf.CAMERA_FRAMERATE) + " -i " + filename + " -c copy " + filename.replace("h264", "mp4")], shell=True) # output file

def cutMP4(filename, start, duration, fileOutput):
	filename = filename.replace("h264", "mp4")
	print("[HANDLER] Cutting", filename, "with start=", start, "and duration=", duration, "...")
	# -y overwrite without asking
	# -ss [start] which point to start at
	# -i input file
	# -c copy with this green squares, without this very slow (~23s with s=3 and t=6)
	# -t [duration] how long should be the clip be
	# output file
	callString = "ffmpeg -loglevel quiet -y -ss " + str(round(start, 1)) + " -i " + filename + " -c copy "
	if duration != None: 
		callString += " -t " + str(duration)
	callString += " " + fileOutput

	subprocess.call([callString], shell=True) # output file

def concatenateMP4(filename1, filename2):
	filename1 = filename1.replace("h264", "mp4")
	filename2 = filename2.replace("h264", "mp4")
	print("[HANDLER] Concatening", filename1, "and", filename2, "...")
	# Create intermediate file
	subprocess.call(["echo \"file '" + filename1 + "'\nfile '" + filename2 + "'\" > concat.txt"], shell=True)
	# -y overwrite without asking
	# -i input files to concatenate (http://stackoverflow.com/questions/7333232/concatenate-two-mp4-files-using-ffmpeg)
	# -c copy with this green squares, without this very slow (~23s with s=3 and t=6)
	# output file
	subprocess.call(["ffmpeg -loglevel quiet -y -f concat -i concat.txt -c copy rpi/vid/swingClip.mp4"], shell=True)
	# Remove old file
	#subprocess.call(["rm concat.txt"], shell=True)

# https://bitbucket.org/zakhar/ffvideo/wiki/Home
def createThumbnail(filename):
	target = filename.replace("mp4", "png")
	# get the duration of the provided video file and take the screenshot 1 second after half of the duration
	duration = subprocess.check_output(["ffprobe -loglevel quiet -y -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "+ filename], shell=True).decode("utf-8")
	time = float(duration.split("\n")[0]) / 2 + 1;
	print(str(time))
	if time < 10 :
		timeString = '00:00:0' + str(round(time)) + '.00'
	elif time > 10 :
		timeString = '00:00:' + str(round(time)) + '.00'
	# create the screenshot
	subprocess.call(["ffmpeg -loglevel quiet -y -i " + filename + " -ss " + timeString +" -vframes 1 " + target], shell=True)

def combineMP4withWAV(videoname, soundname):
	# -itsoffset 00:00:00.00 to delay audio
	# -vcodec & -acodec define video and audio codec used
	subprocess.call(['ffmpeg -loglevel quiet -y -i ' + videoname + ' -i ' + soundname + ' -c:v copy -c:a aac videoname'], shell = True)

if __name__ == '__main__':
	# Value: d for double precision float, b for boolean, i for int
	# Each value gives the timestamp when it last happened
	triggerMotion1 = conf.CAMERA_TRIGGER_MOTION1
	triggerSound = conf.SOUND_TRIGGER_SOUND
	processCameraPi = mp.Process(name="processCameraPi", target=start_record, args=(triggerMotion1, conf.CAMERA_FILENAMES_TS1))
	processCameraMD = mp.Process(name="processCameraMD", target=start_md, args=(2, triggerMotion1, conf.CAMERA_FILENAMES1, conf.CAMERA_FILENAMES_TS1))
	#processSound = mp.Process(name="processSound", target=start_listening, args=(triggerSound, conf.PREP_FILE_LENGTH/60, 'rpi/sound/','.wav'))
	processSound = mp.Process(name="processSound", target=start_listening, args=(triggerSound,))
	#processSound = mp.Process(name="processSound", target=start_recording, args=(triggerSound, conf.AUDIO_FILENAMES_TS))

	# processCameraPi.daemon = True
	processCameraMD.daemon = True
	processSound.daemon = True
	
	processCameraPi.start()
	#processCameraMD.start()
	processSound.start()

	print("[HANDLER] Handler is listening...")
	
	lastSwingRecorded = -1
	while True:
		# If the two triggers happen within a second of each other
		if (triggerMotion1.value > 0 and
		   triggerSound.value > 0 and 
		   abs(triggerMotion1.value-triggerSound.value) <= 1 
		   ):

			if triggerSound.value - lastSwingRecorded > conf.HANDLER_MIN_SWING_DELAY:

				# Use timestamp of sound to create x second clip with ffmpeg
				createSwingClip(triggerSound.value, conf.CAMERA_FILENAMES_TS1)

				# For prep: write timestamp to csv
				#fd = open("swingDetections.csv", "a")
				#fd.write(str(int(triggerSound.value)) + "\n")
				#fd.close()

				lastSwingRecorded = time.time()

			# Reset timestamps after cutting in case of false positives
			triggerMotion1.value = -1
			triggerSound.value = -1

		else:
			time.sleep(0.1)
