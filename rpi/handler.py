
import multiprocessing as mp
import time
import sys
import subprocess

from camera import start_record
from soundListenerUSB import start_listening
import golfConfig as conf

clipStartToMiddleDuration = 3
clipMiddleToEndDuration = 3

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
	print("Swing ts:", tsMiddle)

	# first check file that part of the clip must be in
	# this file can either contain the complete clip (1), the first part (2) or the second part (3)
	# (1) |--------+++++-cap1--------------|-------------cap2--------------|
	#                ^
	# (2) |--------------cap1-----------+++|++-----------cap2--------------|
	#                                     ^ 
	# (3) |--------------cap1------------++|+++----------cap2--------------|
	#                                       ^    

	# First find the file
	filename1 = ""
	diffToFirstClipStart = -1

	for i in range(len(cameraFilenameTS)): 
		diffToFirstClipStart = tsMiddle - cameraFilenameTS[i]
		if diffToFirstClipStart <= conf.CAMERA_CAP_LEN:
			print("FOUND STARTING FILE") # test this assumption
			filename1 = conf.CAMERA_FILENAMES[i]
			break


	# Next check which case we are in
	if diffToFirstClipStart >= clipStartToMiddleDuration:
		# Either (1) or (2)
		if conf.CAMERA_CAP_LEN - diffToFirstClipStart >= clipMiddleToEndDuration:
			# (1) ==> this file is sufficient 
			print("CASE1: no concat necessary")
		else:
			# (2) ==> must retrieve something from the following clip
			print("CASE2: retrieve something from following clip")
	else:
		# (3) ==> we must retrieve something from the previous clip
			print("CASE3: retrieve something from previous clip")

	#subprocess.Popen(["ffmpeg", ])




if __name__ == '__main__':
	# Value: d for double precision float, b for boolean, i for int
	# Each value gives the timestamp when it last happened
	triggerMotion = conf.CAMERA_TRIGGER_MOTION
	triggerSound = conf.SOUND_TRIGGER_SOUND

	processCamera = mp.Process(name="processCamera", target=start_record, args=(triggerMotion, conf.CAMERA_FILENAMES_TS))
	processSound = mp.Process(name="processSound", target=start_listening, args=(triggerSound,))

	processCamera.daemon = True
	processSound.daemon = True

	processCamera.start()
	processSound.start()

	while True:
		# If the two triggers happen within a second of each other
		if triggerMotion.value > 0 and triggerSound.value > 0 and abs(triggerMotion.value-triggerSound.value) <= 1:
			# Reset timestamps before cutting in case of false positives
			triggerMotion.value = -1
			triggerSound.value = -1

			# Use timestamp of sound to create x second clip with ffmpeg
			createSwingClip(triggerSound.value, conf.CAMERA_FILENAMES_TS)


		else:
			#print("done")
			time.sleep(0.1)


	#print("Sleeping...")
	#time.sleep(2)
	#print("Done")
