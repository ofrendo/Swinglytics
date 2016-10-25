import sys
import time
import getopt
import alsaaudio  
import wave  
import numpy
import golfConfig as conf

def start_listening(triggerSound, minutes, folderName, fileEnding):
    print("############################ SOUND ###############################")
    print("Starting to listen with threshold=", conf.SOUND_THRESHOLD)
    print("##################################################################")

    # select the default audio card
    card = 'default'

    # Open the device in nonblocking capture mode. The last argument could
    # just as well have been zero for blocking mode. Then we could have
    # left out the sleep call in the bottom of the loop

    # see alsaaudio.cards() for audio cards and alsaaudio.pcms() for param to give to .PCM()
    # this selects the default card inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, "sysdefault:CARD=Audio")

    # Set attributes: Mono, 44100 Hz, 16 bit little endian samples
    inp.setchannels(1)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    # For our purposes, it is suficcient to know that reads from the device
    # will return this many frames. Each frame being 2 bytes long.
    # This means that the reads below will return either 320 bytes of data
    # or 0 bytes of data. The latter is possible because we are in nonblocking
    # mode.
    inp.setperiodsize(1024)


    while True:
        # reset total frames before each loop
        total = 0
        # create a wave writer to write the sound to a file
        dest = folderName + str(time.time()) + fileEnding
        print("Writing to file: " + dest)
        w = wave.open(dest,'w')
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)

        # 60 * 44100 to record 1 minute of audio
        while total < minutes * 60 * 44100:
            l, data = inp.read()
            try:
                a = numpy.fromstring(data, dtype='int16')
            except:
                print(data)
            val = numpy.abs(a).mean()
            if val > conf.SOUND_THRESHOLD:
                triggerSound.value = time.time()
                print("Sound trigger", val, " at ", triggerSound.value, " with prepAudio")
            if l:
                total += l
                w.writeframes(data)
                time.sleep(.001)
        w.close()
    
if __name__ == '__main__':
    minutes = 0.1
    folder = 'rpi/sound/'
    ending = '.wav'
    start_listening(conf.SOUND_TRIGGER_SOUND, minutes, folder, ending)
