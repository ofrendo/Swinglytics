import multiprocessing as mp
import time
import sys
import subprocess
from pathlib import Path

#if __name__ == '__main__' and __package__ is None:
#	import_parents(level=2)
#	top = Path(__file__).resolve().parents[2]#
#	sys.path.append(str(top))
#	print(top)
#	import prepRecord
#	__package__ = 'rpi.prepRecord'

#from camera import start_record
from multi_camera import start_record
#from .. import soundListenerUSB import start_listening
import golfConfig as conf

def printSwingConsoleMessage():
	print("  ____          _                                          _          _ _ ")
	print(" / ___|_      _(_)_ __   __ _   _ __ ___  ___ ___  _ __ __| | ___  __| | |")
	print(" \___ \ \ /\ / / | '_ \ / _` | | '__/ _ \/ __/ _ \| '__/ _` |/ _ \/ _` | |")
	print("  ___) \ V  V /| | | | | (_| | | | |  __/ (_| (_) | | | (_| |  __/ (_| |_|")
	print(" |____/ \_/\_/ |_|_| |_|\__, | |_|  \___|\___\___/|_|  \__,_|\___|\__,_(_)")
	print("                        |___/                                             ")



if __name__ == '__main__':

	# Value: d for double precision float, b for boolean, i for int
	# Each value gives the timestamp when it last happened
	triggerMotion1 = conf.CAMERA_TRIGGER_MOTION1
	triggerMotion2 = conf.CAMERA_TRIGGER_MOTION2
	triggerSound = conf.SOUND_TRIGGER_SOUND

	processCamera1 = mp.Process(name="processCamera", target=start_record, args=(1, triggerMotion1, conf.CAMERA_FILENAMES1, conf.CAMERA_FILENAMES_TS1))
	processCamera2 = mp.Process(name="processCamera", target=start_record, args=(2, triggerMotion2, conf.CAMERA_FILENAMES2, conf.CAMERA_FILENAMES_TS2))
	#processSound = mp.Process(name="processSound", target=start_listening, args=(triggerSound,))

	processCamera1.daemon = True
	processCamera2.daemon = True
	#processSound.daemon = True

	processCamera1.start()
	processCamera2.start()
	#processSound.start()

	print("Handler is listening...")

	while True:
		# If the two triggers happen within a second of each other
		if (triggerMotion1.value > 0 and
		   triggerMotion2.value > 0 and 
		   triggerSound.value > 0 and 
		   abs(triggerMotion1.value-triggerMotion2.value) <= 1 and
		   abs(triggerMotion1.value-triggerSound.value) <= 1 and
		   abs(triggerMotion2.value-triggerSound.value) <= 1):
			# Use timestamp of sound to create x second clip with ffmpeg
			#createSwingClip(triggerSound.value, conf.CAMERA_FILENAMES_TS)

			# Reset timestamps before cutting in case of false positives
			triggerMotion1.value = -1
			triggerMotion2.value = -1
			triggerSound.value = -1

			# For prep: write timestamp to csv
			printSwingConsoleMessage()

		else:
			time.sleep(0.1)