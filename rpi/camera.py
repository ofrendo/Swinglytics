# http://picamera.readthedocs.io/en/release-1.12/recipes2.html#custom-outputs
# http://picamera.readthedocs.io/en/release-1.12/api_array.html#pimotionanalysis


import multiprocessing as mp
import picamera
import picamera.array
import numpy as np
import itertools
import time

RESOLUTION = (1024, 768)
FRAMERATE = 30
FILENAMES = ("rpi/vid/cap1.h264", "rpi/vid/cap2.h264")
CAP_LEN = 10 # how long should each capture be

THRESHOLD = 60
MIN_NUMBER_MOTION_VECTORS = 20

class SimpleMotionAnalyzer(picamera.array.PiMotionAnalysis):
    def __init__(self, camera, triggerMotion):
        super().__init__(camera)
        self.triggerMotion = triggerMotion

    # this needs to take less than the time between frames, e.g. 33ms for 30fps
    # better to put into queue for other thread
    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (a > THRESHOLD).sum() > MIN_NUMBER_MOTION_VECTORS:
            ts = time.time()
            print("Motion detected at", ts)
            # Save/trigger timestamp of motion to shared variable
            self.triggerMotion.value = ts
            
            

def start_record(triggerMotion):
    print("########################### CAMERA ##############################")
    print("Starting camera recording at", RESOLUTION[0], "x", RESOLUTION[1], "with", FRAMERATE, "fps...")
    print("Motion detection: threshold=", THRESHOLD, " min_number_motion_vectors=", MIN_NUMBER_MOTION_VECTORS)
    print("##################################################################")

    camera = picamera.PiCamera()
    camera.resolution = RESOLUTION # might need to reduce this
    camera.framerate = FRAMERATE

    # Record motion data to our custom output object
    for filename in camera.record_sequence(
            itertools.cycle(FILENAMES), 
            format="h264", 
            motion_output=SimpleMotionAnalyzer(camera, triggerMotion)
        ):
        print('Recording to %s' % filename)
        camera.wait_recording(CAP_LEN)
            

if __name__ == '__main__':
    # Only executed if explicitely calling this file: use for testing purposes
    triggerMotion = mp.Value("d", -1)
    start_record(triggerMotion) 
