# http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation

import time
import boto3
from botocore.client import Config
import json
import requests

import golfConfig as conf

# constants
BUCKET_NAME = "hopinone"

# connections
s3 = boto3.resource("s3", config=Config(signature_version='s3v4'))
bucket = s3.Bucket(BUCKET_NAME)




def uploadFile(filename, tsMiddle): 
	key = "swingClip_" + str(conf.STATION_ID) + "_" + str(int(tsMiddle)) + ".mp4"
	print("[STORAGE] Uploading", filename, "with key=", key, "to cloud...")
	startTime = time.time()
	data = open(filename, "rb")
	bucket.put_object(Key=key, Body=data, ACL="public-read")
	dt = time.time() - startTime
	print("[STORAGE] Uploaded file in", dt)


	print("[STORAGE] Making POST request to server...")
	payload = {"stationID": conf.STATION_ID, "ts": tsMiddle}
	headers = {"content-type": "application/json"}
	url = conf.SERVER_URL + "/post"
	response = requests.post(url, data=json.dumps(payload), headers=headers)
	print("[STORAGE] Made POST request.")
	print(response)
	

if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes
	uploadFile("rpi/test/test_ser10.mp4", "testFile")
