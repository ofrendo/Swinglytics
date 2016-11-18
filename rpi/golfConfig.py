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
AUDIO_DURATION_SECONDS = 10
RECORD_FOLDER = "rpi/vid/"
AUDIO_ENDING = ".wav"

## Sound stuff
SOUND_THRESHOLD = 600 # how loud does the noise have to be
SOUND_TRIGGER_SOUND = mp.Value("d", -1)
SOUND_CHANNELS = 1
SOUND_RATE = 44100 #22050
SOUND_CHUNKSIZE = 1024
AUDIO_FILENAMES = ("rpi/vid/cap1_1" + AUDIO_ENDING, 
             "rpi/vid/cap1_2" + AUDIO_ENDING,
             "rpi/vid/cap1_3" + AUDIO_ENDING,
             "rpi/vid/cap1_4" + AUDIO_ENDING)
AUDIO_FILENAMES_TS = mp.Array("d", [-1, -1, -1, -1])


## Motion Detection Stuff
height = 304 * 0.75 # 75% takes the rescaling of the frame into consideration
width = 400 * 0.75 # 75% takes the rescaling of the frame into consideration
MOTION_X_MIN = int(width * 0.25) #75
MOTION_X_MAX = int(width * 0.75) #225
MOTION_Y_MIN = int(height * 0.1) #25
MOTION_Y_MAX = int(height * 0.9) #200

## Handler stuff
HANDLER_MIN_SWING_DELAY = 1


## Networking stuff
STATION_ID = 1
#SERVER_URL = "http://httpbin.org" # test page, will return anything sent to it
#SERVER_URL = "http://138.68.108.39:3000" # digital ocean server
SERVER_URL = "http://192.168.178.76:3000" # desktop pc at home
#SERVER_URL = "https://192.168.188.26:3000" # laptop in mobile

SERVER_USE_FTP = True  # Should ftp be used for file upload? If false AWS will be used
SERVER_FTP = "192.168.178.76" # desktop pc at home
#SERVER_FTP = "192.168.188.26"


## Prep stuff
PREP_FILE_LENGTH = 10*60











