# Enable ssh and camera
```
sudo raspi-config
```
Navigate to advanced/ssh and enable it

# Change password for "pi" user` 
```
sudo -i
passwd pi
```

# SSH key generation for github
```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install vim
```


# Remote desktop (see http://raspberrypi.stackexchange.com/questions/56413/error-problem-connecting-to-raspberry-pi-3-with-xrdp)
```
sudo apt-get remove xrdp vnc4server tightvncserver
sudo apt-get install tightvncserver
sudo apt-get install xrdp
```

# ffmpeg installation: see https://github.com/ccrisan/motioneye/wiki/Install-On-Raspbian
```
sudo apt-get install python-pip python-dev curl libssl-dev libcurl4-openssl-dev libjpeg-dev libx264-142
wget https://github.com/ccrisan/motioneye/wiki/precompiled/ffmpeg_3.1.1-1_armhf.deb
sudo dpkg -i ffmpeg_3.1.1-1_armhf.deb
```

# opencv installation: see http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
```
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
```

THIS FAILS because of previous ffmpeg installation (see http://www.webupd8.org/2011/02/fix-dpkg-error-trying-to-overwrite-x.html)
```
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
```
To fix run this:
``` 
sudo dpkg -i --force-overwrite  /var/cache/apt/archives/libavutil-dev_6%3a11.8
-1~deb8u1+rpi1_armhf.deb
sudo dpkg -i --force-overwrite /var/cache/apt/archives/libavcodec-dev_6%3a11.8
-1~deb8u1+rpi1_armhf.deb
sudo dpkg -i --force-overwrite /var/cache/apt/archives/libavformat-dev_6%3a11.
8-1~deb8u1+rpi1_armhf.deb
 sudo dpkg -i --force-overwrite /var/cache/apt/archives/libswscale-dev_6%3a11
.8-1~deb8u1+rpi1_armhf.deb
```
To continue:
```
sudo apt-get install libgtk2.0-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3-dev
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
unzip opencv_contrib.zip

sudo pip3 install virtualenv virtualenvwrapper
```
This next part doesnt seem to work for python3
```
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
mkvirtualenv cv -p python3
```
```
cd ~/opencv-3.1.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
	-D WITH_FFMPEG=OFF \
    -D BUILD_EXAMPLES=ON .. 
```
If the following fails, try "make clean" and then "make"
```
make -j4
sudo make install
sudo ldconfig

cd /usr/local/lib/python3.4/dist-packages/
sudo mv cv2.cpython-34m.so cv2.so
```

# Python packages
```
sudo pip3 install picamera

sudo apt-get install libjack-jackd2-dev portaudio19-dev
sudo pip3 install pyalsaaudio
sudo pip3 install pyaudio
sudo pip3 install boto3
sudo pip3 install imutils
sudo pip3 install urllib2

sudo apt-get install python-dev cython libavcodec-dev libavformat-dev libswscale-dev python-pip
sudo pip3 install ffvideo
```


# AWS
```
mkdir ~/.aws
touch ~/.aws/credentials
vim ~/.aws/credentials
[default]
...
...
```

## Web login
https://is613dt.signin.aws.amazon.com/console
...


# Git
``` 
git config --global user.email "ofrendo@gmail.com"
git config --global user.name "Oliver Frendo"
git config --global push.default simple
```

# testing sound (not needed)
```
pacmd

sudo aplay -L
sudo aplay /usr/share/sounds/alsa/Front_Center.wav
sudo speaker-test -Dsurround21:Audio -c 2

lspci -v | grep -A7 -i "audio"
sudo modprobe snd-usb-[NAME OF YOUR SOUNDCARD'S DRIVER]
```