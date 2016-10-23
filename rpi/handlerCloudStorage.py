# http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation

import sys
import time
import boto3
from botocore.client import Config
import json
import requests

import golfConfig as conf
import ftplib

# constants
BUCKET_NAME = "hopinone"

# connections
s3 = boto3.resource("s3", config=Config(signature_version='s3v4'))
bucket = s3.Bucket(BUCKET_NAME)


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

def uploadFile(filename, tsMiddle): 
	key = "swingClip_" + str(conf.STATION_ID) + "_" + str(int(tsMiddle)) + ".mp4"

	if conf.SERVER_USE_FTP == False:
		uploadFileAWS(filename, key)
	else:
		uploadFileFTP(filename, key)


	print("[STORAGE] Making POST request to server...")
	payload = {"stationID": conf.STATION_ID, "ts": tsMiddle}
	headers = {"content-type": "application/json"}
	url = conf.SERVER_URL + "/post"
	response = requests.post(url, data=json.dumps(payload), headers=headers)
	print("[STORAGE] Made POST request.")
	print(response)
	#print(response.text)
	

if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes
	# command line args: "ftp", or aws=none

	if len(sys.argv)>1 and sys.argv[1] == "ftp":
		conf.SERVER_USE_FTP = True

	uploadFile("rpi/vid/swingClip.mp4", time.time())
