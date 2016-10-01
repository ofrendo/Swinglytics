
import multiprocessing as mp
import time

from camera import start_record
from clap import start_listening



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
		if triggerMotion.value > 0 and triggerSound.value > 0 and abs(triggerMotion-triggerSound) <= 1:
			# Use timestamp of sound to create x second clip with ffmpeg
			print("Here")
		else:
			print("done")
			time.sleep(5)
			break


	#print("Sleeping...")
	#time.sleep(2)
	#print("Done")
