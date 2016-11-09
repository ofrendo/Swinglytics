# http://stackoverflow.com/questions/6867675/audio-recording-in-python
#w = wave.open('test.wav', 'w')
#w.setnchannels(1)
#w.setsampwidth(2)
#w.setframerate(44100)
#w.writeframes(data)
#import wave

import alsaaudio
import pyaudio
import numpy
import time
import wave
import struct
from sys import byteorder
from array import array
import multiprocessing as mp

import golfConfig as conf

def getFileIndex(filename):
    for i in range(len(conf.AUDIO_FILENAMES)):
        if filename == conf.AUDIO_FILENAMES[i]:
            return i

def start_listening(triggerSound):
	print("############################ SOUND ###############################")
	print("Starting to listen with threshold=", conf.SOUND_THRESHOLD)
	print("##################################################################")

	# see alsaaudio.cards() for audio cards and alsaaudio.pcms() for param to give to .PCM()
	# this selects the default card inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK) #, "sysdefault:CARD=Audio"
	inp.setchannels(1)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)

	while(True):
		l, data = inp.read()
		a = numpy.fromstring(data, numpy.int16)

		val = numpy.abs(a).mean()
		if val > conf.SOUND_THRESHOLD:
			triggerSound.value = time.time()
			print("[SOUND] Sound trigger", val, " at ", triggerSound.value)

def start_recording(triggerSound, audioFilenameTS):
	CHUNKSIZE = 1024
	FORMAT = pyaudio.paInt16
	RATE = 44100
	CHANNELS = 1
	p = pyaudio.PyAudio()
	stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNKSIZE)
	for filename in conf.AUDIO_FILENAMES:
		print("########################### AUDIO ##############################")
		print("Recording to file: " + filename)
		print("#################################################################")
		data_all = array('h')
		blocks = int(RATE * conf.AUDIO_DURATION_SECONDS / CHUNKSIZE)
		for i in range(0, blocks):
			# ignoring overflow of array based on reading too slow from the input
			data_chunk = array('h', stream.read(CHUNKSIZE, exception_on_overflow = False))
			if byteorder == 'big':
				data_chunk.byteswap()
			data_all.extend(data_chunk)
			val = max(data_chunk)

			if val > conf.SOUND_THRESHOLD:
				triggerSound.value = time.time()
				i = getFileIndex(filename)
				audioFilenameTS[i] = time.time()
				print("[SOUND] Sound trigger", val, " at ", triggerSound.value)

		w = wave.open(filename, 'w')
		w.setnchannels(1)
		w.setsampwidth(2)
		w.setframerate(44100)
		w.setnframes(conf.AUDIO_DURATION_SECONDS * 44100)
		w.writeframes(data_all)
		w.close()





if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes

	start_listening(conf.SOUND_TRIGGER_SOUNDS)
	# start_recording(conf.SOUND_TRIGGER_SOUNDS, conf.AUDIO_FILENAMES_TS)
   
