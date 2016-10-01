# http://picamera.readthedocs.io/en/release-1.12/recipes2.html#custom-outputs
# http://picamera.readthedocs.io/en/release-1.12/api_array.html#pimotionanalysis


import multiprocessing as mp
import picamera
import picamera.array
import numpy as np
import itertools
import time

import golfConfig as conf


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
        if (a > conf.CAMERA_MOTION_THRESHOLD).sum() > conf.CAMERA_MIN_NUMBER_MOTION_VECTORS:
            ts = time.time()
            print("Motion detected at", ts)
            # Save/trigger timestamp of motion to shared variable
            self.triggerMotion.value = ts
            
def getFileIndex(filename):
    for i in range(len(conf.CAMERA_FILENAMES)):
        if filename == conf.CAMERA_FILENAMES[i]:
            return i

def start_record(triggerMotion, cameraFilenameTS):
    print("########################### CAMERA ##############################")
    print("Starting camera recording at", conf.CAMERA_RESOLUTION[0], "x", conf.CAMERA_RESOLUTION[1], "with", conf.CAMERA_FRAMERATE, "fps...")
    print("Motion detection: threshold=", conf.CAMERA_MOTION_THRESHOLD, " min_number_motion_vectors=", conf.CAMERA_MIN_NUMBER_MOTION_VECTORS)
    print("##################################################################")

    camera = picamera.PiCamera()
    camera.resolution = conf.CAMERA_RESOLUTION # might need to reduce this
    camera.framerate = conf.CAMERA_FRAMERATE

    # Record motion data to our custom output object
    for filename in camera.record_sequence(
            itertools.cycle(conf.CAMERA_FILENAMES), 
            format="h264", 
            # format="yuv", with this we can't use motion detection
            motion_output=SimpleMotionAnalyzer(camera, triggerMotion)
        ):
        i = getFileIndex(filename)
        cameraFilenameTS[i] = time.time()

        print("Recording to",  filename, "at", time.time())
        camera.wait_recording(conf.CAMERA_CAP_LEN)
            

if __name__ == '__main__':
    # Only executed if explicitely calling this file: use for testing purposes
    start_record(conf.CAMERA_TRIGGER_MOTION, conf.CAMERA_FILENAMES_TS) 
