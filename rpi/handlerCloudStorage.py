# http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation

import sys
import time
import boto3
from botocore.client import Config
import json
import requests
from random import randint

import golfConfig as conf
import ftplib
import json



# constants
BUCKET_NAME = "hopinone"

# connections
s3 = boto3.resource("s3", config=Config(signature_version='s3v4'))
bucket = s3.Bucket(BUCKET_NAME)


# see http://stackoverflow.com/questions/2673385/how-to-generate-random-number-with-the-specific-length-in-python
def random_with_N_digits(n):
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start, range_end)


# Sends a GET request for this station to check if a user is currently logged in
def sendLoginCheck():
	url = conf.SERVER_URL + "/api/v1/checkuser/" + str(conf.STATION_ID)
	response = requests.get(url)
	body = response.json()
	#print(body["userID"])
	return body["userID"]


def uploadFileAWS(filename, key):
	print("[STORAGE] Uploading", filename, "with key=", key, "to AWS...")
	startTime = time.time()
	data = open(filename, "rb")
	bucket.put_object(Key=key, Body=data, ACL="public-read")
	dt = time.time() - startTime
	print("[STORAGE] Uploaded file to AWS  in", dt)


def uploadFileFTP(filename, key):
	print("[STORAGE] Uploading", filename, "with key=", key, "to FTP...")
	ftp = ftplib.FTP(conf.SERVER_FTP)
	ftp.login("rpi", "is613dt")

	startTime = time.time()
	data = open(filename, "rb")
	ftp.storbinary("STOR " + key, data, 1024)
	
	dt = time.time() - startTime
	print("[STORAGE] Uploaded file to FTP  in", dt)

def uploadFile(videoName, thumbnailName, tsMiddle, loginCheck=True):
	# Check if a user is logged in before submitting a video
	userID = None
	if (loginCheck == True):
		userID = sendLoginCheck() 
		if (userID == ""):
			print("[STORAGE] No user is currently logged in.")
			return
		else:
			print("[STORAGE] User", userID, "is logged in.")
	else:
		userID = "bob"

	# Key is what the file will be named on the server, for example
	# swingClip_{stationID}_{timestamp}_{random}.mp4
	random = random_with_N_digits(5)
	tsMiddle = int(tsMiddle)
	keyVideo = "swingClip_" + str(conf.STATION_ID) + "_" + str(tsMiddle) + "_" + str(random) + ".mp4"
	keyThumbnail = "swingClip" + str(conf.STATION_ID) + "_" + str(tsMiddle) + "_" + str(random) + ".png"
	if conf.SERVER_USE_FTP == False:
		uploadFileAWS(videoName, keyVideo)
		uploadFileAWS(thumbnailName, keyThumbnail)
	else:
		uploadFileFTP(videoName, keyVideo)
		uploadFileFTP(thumbnailName, keyThumbnail)


	url = conf.SERVER_URL + "/api/v1/video"
	print("[STORAGE] Making POST request to ", url, "...")
	payload = {
		"userID": userID,
		"stationID": conf.STATION_ID, 
		"timestamp": tsMiddle,
		"random": random,
		"signature": "NOT IMPLEMENTED"}
	headers = {"content-type": "application/json"}
	
	response = requests.post(url, data=json.dumps(payload), headers=headers)
	print("[STORAGE] Made POST request.")
	print(response.text)
	#data = response.json()
	#print(data)
	#data2 = json.loads(data["data"])
	#print(data2["stationID"])


if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes
	# command line args: "ftp", or aws=none

	if len(sys.argv)>1 and sys.argv[1] == "ftp":
		conf.SERVER_USE_FTP = True

	uploadFile("rpi/vid/swingClip.mp4", time.time(), False)
