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

import golfConfig as conf

def start_listening(triggerSound):
	print("############################ SOUND ###############################")
	print("Starting to listen with threshold=", conf.SOUND_THRESHOLD)
	print("##################################################################")

	# see alsaaudio.cards() for audio cards and alsaaudio.pcms() for param to give to .PCM()
	# this selects the default card inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, "sysdefault:CARD=Audio")

	inp.setchannels(1)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)

	while True:
		l, data = inp.read()
		a = numpy.fromstring(data, dtype='int16')
		
		val = numpy.abs(a).mean()
		if val > conf.SOUND_THRESHOLD:
			triggerSound.value = time.time()
			print("[SOUND] Sound trigger", val, " at ", triggerSound.value)






if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes
	start_listening(conf.SOUND_TRIGGER_SOUND)
   