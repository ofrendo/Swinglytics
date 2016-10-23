import multiprocessing as mp
import time
import sys
import subprocess

from camera import start_record
from multi_camera import start_md
from prepAudio import start_listening
import golfConfig as conf

def printSwingConsoleMessage():
	print("  ____          _                                          _          _ _ ")
	print(" / ___|_      _(_)_ __   __ _   _ __ ___  ___ ___  _ __ __| | ___  __| | |")
	print(" \___ \ \ /\ / / | '_ \ / _` | | '__/ _ \/ __/ _ \| '__/ _` |/ _ \/ _` | |")
	print("  ___) \ V  V /| | | | | (_| | | | |  __/ (_| (_) | | | (_| |  __/ (_| |_|")
	print(" |____/ \_/\_/ |_|_| |_|\__, | |_|  \___|\___\___/|_|  \__,_|\___|\__,_(_)")
	print("                        |___/                                             ")



if __name__ == '__main__':
	print("Prep record handler is starting...")

	# Value: d for double precision float, b for boolean, i for int
	# Each value gives the timestamp when it last happened
	triggerMotion1 = conf.CAMERA_TRIGGER_MOTION1
	triggerMotion2 = conf.CAMERA_TRIGGER_MOTION2
	triggerSound = conf.SOUND_TRIGGER_SOUND

	processCameraPi = mp.Process(name="processCameraPi", target=start_record, args=(None, conf.CAMERA_FILENAMES_TS1))
	processCameraMD = mp.Process(name="processCameraMD", target=start_md, args=(2, triggerMotion1, conf.CAMERA_FILENAMES1, conf.CAMERA_FILENAMES_TS1))
	processSound = mp.Process(name="processSound", target=start_listening, args=(triggerSound, conf.PREP_FILE_LENGTH/60, 'rpi/sound/','.wav'))

	processCameraPi.daemon = True
	processCameraMD.daemon = True
	processSound.daemon = True

	processCameraPi.start()
	processCameraMD.start()
	processSound.start()

	
	lastSwingRecorded = -1
	while True:
		# If the two triggers happen within a second of each other
		if (triggerMotion1.value > 0 and
		   #triggerMotion2.value > 0 and 
		   triggerSound.value > 0 and 
		   #abs(triggerMotion1.value-triggerMotion2.value) <= 1 and
		   abs(triggerMotion1.value-triggerSound.value) <= 1 
		   #and abs(triggerMotion2.value-triggerSound.value) <= 1
		   ):
			# Use timestamp of sound to create x second clip with ffmpeg
			#createSwingClip(triggerSound.value, conf.CAMERA_FILENAMES_TS)

			if triggerSound.value - lastSwingRecorded > conf.HANDLER_MIN_SWING_DELAY:
				# For prep: write timestamp to csv
				printSwingConsoleMessage()

				fd = open("swingDetections.csv", "a")
				fd.write(str(int(triggerSound.value)) + "\n")
				fd.close()

				lastSwingRecorded = time.time()

			# Reset timestamps after cutting in case of false positives
			triggerMotion1.value = -1
			triggerMotion2.value = -1
			triggerSound.value = -1

			

		else:
			time.sleep(0.1)
