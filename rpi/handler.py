
import multiprocessing as mp
import time
import sys
import subprocess

from camera import start_record
from soundListenerUSB import start_listening

clipStartToMiddleDuration = 3
clipMiddleToEndDuration = 3

def printSwingConsoleMessage():
	print("  ____          _                                          _          _ _ ")
	print(" / ___|_      _(_)_ __   __ _   _ __ ___  ___ ___  _ __ __| | ___  __| | |")
	print(" \___ \ \ /\ / / | '_ \ / _` | | '__/ _ \/ __/ _ \| '__/ _` |/ _ \/ _` | |")
	print("  ___) \ V  V /| | | | | (_| | | | |  __/ (_| (_) | | | (_| |  __/ (_| |_|")
	print(" |____/ \_/\_/ |_|_| |_|\__, | |_|  \___|\___\___/|_|  \__,_|\___|\__,_(_)")
	print("                        |___/                                             ")

def createSwingClip(tsMiddle): 
	printSwingConsoleMessage()
	#subprocess.Popen(["ffmpeg", ])

if __name__ == '__main__':
	# Value: d for double precision float, b for boolean 
	# Each value gives the timestamp when it last happened
	triggerMotion = mp.Value("d", -1) 
	triggerSound = mp.Value("d", -1)

	processCamera = mp.Process(name="processCamera", target=start_record, args=(triggerMotion,))
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
			createSwingClip(triggerSound.value)


		else:
			#print("done")
			time.sleep(0.1)


	#print("Sleeping...")
	#time.sleep(2)
	#print("Done")
