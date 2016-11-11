import multiprocessing as mp

## Camera stuff
CAMERA_RESOLUTION = (1024, 768)  # # #(480, 368)
CAMERA_FRAMERATE = 24
ending = "h264"
CAMERA_FILENAMES1 = ("rpi/vid/cap1_1." + ending, 
             "rpi/vid/cap1_2." + ending,
             "rpi/vid/cap1_3." + ending,
             "rpi/vid/cap1_4." + ending)
CAMERA_FILENAMES2 = ("rpi/vid/cap2_1." + ending, 
             "rpi/vid/cap2_2." + ending,
             "rpi/vid/cap2_3." + ending,
             "rpi/vid/cap2_4." + ending)
CAMERA_FILENAMES_TS1 = mp.Array("d", [-1, -1, -1, -1]) 
CAMERA_FILENAMES_TS2 = mp.Array("d", [-1, -1, -1, -1]) 

CAMERA_CAP_LEN = 10 # how long should each capture be
CAMERA_CAP_LEN_FRAMES = CAMERA_FRAMERATE * CAMERA_CAP_LEN

CAMERA_MOTION_THRESHOLD = 60 # used for pi camera to detect motion
CAMERA_MIN_NUMBER_MOTION_VECTORS = 20

CAMERA_TRIGGER_MOTION1 = mp.Value("d", -1) # saves a shared timestamp when the last motion detection occured (picamera)
CAMERA_TRIGGER_MOTION2 = mp.Value("d", -1) # saves a shared timestamp when the last motion detection occured (action cam)

AUDIO_DURATION_MINUTES = 10 # used for audio recording
RECORD_FOLDER = "rpi/vid/"
AUDIO_ENDING = ".wav"

## Sound stuff
SOUND_THRESHOLD = 400 # how loud does the noise have to be
SOUND_TRIGGER_SOUND = mp.Value("d", -1)



## Handler stuff
HANDLER_MIN_SWING_DELAY = 1


## Networking stuff
STATION_ID = 1
#SERVER_URL = "http://httpbin.org" # test page, will return anything sent to it
SERVER_URL = "http://138.68.108.39:3000" # digital ocean server
#SERVER_URL = "http://192.168.178.76:3000" # desktop pc at home

SERVER_USE_FTP = False  # Should ftp be used for file upload? If false AWS will be used
SERVER_FTP = "192.168.178.76" # desktop pc at home



## Prep stuff
PREP_FILE_LENGTH = 10*60











