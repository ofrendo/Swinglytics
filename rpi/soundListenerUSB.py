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
import audioop
import itertools
from sys import byteorder
from array import array
import multiprocessing as mp

import golfConfig as conf

def getFileIndex(filename):
    for i in range(len(conf.AUDIO_FILENAMES)):
        if filename == conf.AUDIO_FILENAMES[i]:
            return i

# Method used for just listening and triggering sound, not recording it
def start_listening(triggerSound):
	print("############################ SOUND ###############################")
	print("Starting to listen with threshold=", conf.SOUND_THRESHOLD)
	print("##################################################################")

	# see alsaaudio.cards() for audio cards and alsaaudio.pcms() for param to give to .PCM()
	# this selects the default card inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK) #, "sysdefault:CARD=Audio"
	inp.setchannels(conf.SOUND_CHANNELS)
	inp.setrate(conf.SOUND_RATE)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(conf.SOUND_CHUNKSIZE)

	lastTriggerMessage = -1
	while(True):
		l, data = inp.read()
		a = numpy.fromstring(data, numpy.int16)

		val = numpy.abs(a).mean()
		if val > conf.SOUND_THRESHOLD:
			triggerSound.value = time.time()
			if (triggerSound.value - lastTriggerMessage > 0.1):
				lastTriggerMessage = time.time()
				print("[SOUND] Sound trigger", val, " at ", triggerSound.value)

# Method used for Raspberry Pi 3
def start_recording_alsa(triggerSound, audioFilenameTS):
	print("############################ SOUND ###############################")
	print("Starting to listen with threshold=", conf.SOUND_THRESHOLD)
	print("##################################################################")
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK) #, "sysdefault:CARD=Audio"
	inp.setchannels(conf.SOUND_CHANNELS)
	inp.setrate(conf.SOUND_RATE)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(conf.SOUND_CHUNKSIZE)
	
	lastTriggerMessage = -1 # when was the trigger message last written to the console?
	currentFileIndex = -1 # which file is being written to currently?
	for filename in itertools.cycle(conf.AUDIO_FILENAMES):
		i = getFileIndex(filename)
		audioFilenameTS[i] = time.time()	
		currentFileIndex = i # change to match camera

		print("[SOUND] Recording to file: " + filename + ", file index=" + str(currentFileIndex))
		total = 0
		w = wave.open(filename, 'w')
		w.setnchannels(conf.SOUND_CHANNELS)
		w.setsampwidth(2)
		w.setframerate(conf.SOUND_RATE*2)
		w.setnframes(conf.CAMERA_CAP_LEN * conf.SOUND_RATE)

		while currentFileIndex == conf.CAMERA_TRIGGER_FILENAMES_INDEX.value: #total < conf.SOUND_RATE * conf.CAMERA_CAP_LEN:
			l, data = inp.read()

			# Write data to file
			if l:
				total += l
				w.writeframes(data)

			# Check if threshold was reached
			# How many bytes should be read? Max 32, if this part is too slow the length can also be larger
			count = -1
			dataLen = len(data)
			if (dataLen < 32):
				count = 0
			else:
				count = 32

			a = numpy.fromstring(data, dtype=numpy.int16, count=count)
			val = numpy.abs(a).mean()
			if val > conf.SOUND_THRESHOLD:
				triggerSound.value = time.time()

				if (triggerSound.value - lastTriggerMessage > 0.1):
					lastTriggerMessage = time.time()
					print("[SOUND] Sound trigger", val, " at ", triggerSound.value)
		w.close()

# Method used for Banana Pi
def start_recording(triggerSound, audioFilenameTS):
	chunksize = conf.SOUND_CHUNKSIZE
	format = pyaudio.paInt16
	rate = conf.SOUND_RATE
	channels = conf.SOUND_CHANNELS
	p = pyaudio.PyAudio()
	stream = p.open(format = format, channels = channels, rate = rate, input = True, output = True, frames_per_buffer = chunksize)
	for filename in conf.AUDIO_FILENAMES:
		print("########################### AUDIO ##############################")
		print("Recording to file: " + filename)
		print("#################################################################")
		data_all = array('h')
		blocks = int(rate * conf.AUDIO_DURATION_SECONDS / chunksize)
		for i in range(0, blocks):
			# ignoring overflow of array based on reading too slow from the input
			data_chunk = array('h', stream.read(chunksize, exception_on_overflow = False))
			if byteorder == 'big':
				data_chunk.byteswap()
			data_all.extend(data_chunk)
			val = audioop.rms(data_chunk, 2)

			if val > conf.SOUND_THRESHOLD:
				triggerSound.value = time.time()
				i = getFileIndex(filename)
				audioFilenameTS[i] = time.time()
				print("[SOUND] Sound trigger", val, " at ", triggerSound.value)

		w = wave.open(filename, 'w')
		w.setnchannels(channels)
		w.setsampwidth(2)
		w.setframerate(rate)
		w.setnframes(conf.AUDIO_DURATION_SECONDS * rate)
		w.writeframes(data_all)
		w.close()



if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes

	#start_listening(conf.SOUND_TRIGGER_SOUND)
	#start_recording(conf.SOUND_TRIGGER_SOUND, conf.AUDIO_FILENAMES_TS)
	start_recording_alsa(conf.SOUND_TRIGGER_SOUND, conf.AUDIO_FILENAMES_TS)
   
