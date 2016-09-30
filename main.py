# http://picamera.readthedocs.io/en/release-1.12/recipes2.html#custom-outputs

import picamera
import picamera.array
import numpy as np
import itertools


FILENAMES = ("cap1.h264", "cap2.h264")
CAP_LEN = 10


class MyMotionDetector(picamera.array.PiMotionAnalysis):
	# this needs to take less than the time between frames, e.g. 33ms for 30fps
    # better to put into queue for other thread
    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (a > 60).sum() > 10:
            print('Motion detected!')
			# Save/trigger timestamp of motion to disk/env variable	
			
			
camera = picamera.PiCamera()
camera.resolution = (1024, 768) # might need to reduce this
camera.framerate = 30

# Record motion data to our custom output object
for filename in camera.record_sequence(format="h264", itertools.cycle(FILENAMES), motion_output=SimpleMotionDetector(camera)):
	print('Recording to %s' % filename)
    camera.wait_recording(CAP_LEN)
	