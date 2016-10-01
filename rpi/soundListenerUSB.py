# http://stackoverflow.com/questions/6867675/audio-recording-in-python
#w = wave.open('test.wav', 'w')
#w.setnchannels(1)
#w.setsampwidth(2)
#w.setframerate(44100)
#w.writeframes(data)
#import wave

import alsaaudio
import numpy
import time
import multiprocessing as mp


def start_listening(triggerSound):
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
	inp.setchannels(1)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)

	while True:
		l, data = inp.read()
		a = numpy.fromstring(data, dtype='int16')
		
		val = numpy.abs(a).mean()
		if val > 150:
			triggerSound.value = time.time()
			print("Clapped: ", val, " at ", triggerSound.value)






if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes
	triggerSound = mp.Value("d", -1)
	start_listening(triggerSound)
   