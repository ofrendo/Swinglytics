
import multiprocessing as mp
import time
import sys
import subprocess

from camera import start_record
from soundListenerUSB import start_listening

clipStartToMiddleDuration = 3
clipMiddleToEndDuration = 3

def createSwingClip(tsMiddle): 
	print("Recorded swing. Cutting and saving file...")
	subprocess.Popen(["ffmpeg", ])

if __name__ == '__main__':
	# Value: d for double precision float, b for boolean 
	# Each value gives the timestamp when it last happened
	triggerMotion = mp.Value("d", -1) 
	triggerSound = mp.Value("d", -1)

	processCamera = mp.Process(name="processCamera", target=start_record, args=(triggerMotion,))
	processSound = mp.Process(name="processSound", target=start_listening, args=(triggerSound,))

	processCamera.daemon = True
	processSound.daemon = True

	#processCamera.start()
	processSound.start()

	while True:
		# If the two triggers happen within a second of each other
		if triggerMotion.value > 0 and triggerSound.value > 0 and abs(triggerMotion.value-triggerSound.value) <= 1:
			# Use timestamp of sound to create x second clip with ffmpeg
			createSwingClip(triggerSound.value)
		else:
			print("done")
			time.sleep(5)
			break


	#print("Sleeping...")
	#time.sleep(2)
	#print("Done")
