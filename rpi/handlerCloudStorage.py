# http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation

import sys
import time
import boto3
from botocore.client import Config
import json
import requests
from random import randint
import ftplib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

import golfConfig as conf

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

def generateSignature(plaintext):
	# SOURCE
	# SHA256 of plaintext
	plaintext = "1_1477334965_68865"
	h = SHA256.new()
	h.update(bytes(plaintext, "utf-8"))
	hash = h.hexdigest()
	print("Hashing:", plaintext)
	print("Hash:", hash)

	# http://stackoverflow.com/questions/21327491/using-pycrypto-how-to-import-a-rsa-public-key-and-use-it-to-encrypt-a-string
	# Then encrypt hash with private key as signature
	path = "/home/pi/.ssh/id_rsa_private.pem"
	f = open(path, "r")
	privKey = RSA.importKey(f.read())
	
	# Textbook RSA, no padding
	encrypted = privKey.encrypt(bytes(hash, "utf-8"), "unneeded")[0]
	result = str(binascii.hexlify(encrypted))[1:] #  the 1: removes "b" infront of string, because its a byte string http://stackoverflow.com/questions/17013089/python-get-rid-of-bytes-b
	
	# RSA with padding:
	#cipher = PKCS1_OAEP.new(privKey)
	#encrypted = cipher.encrypt(bytes(hash, "utf-8"))
	#result = str(binascii.hexlify(encrypted))[1:] #  the 1: removes "b" infront of string, because its a byte string http://stackoverflow.com/questions/17013089/python-get-rid-of-bytes-b
	
	#result = encrypted.encode('hex') 

	print("Encrypted: ", result)
	return (plaintext, hash, result)
	# On server decrypt hash with public key
	# generate hash of plaintext
	# Compare: if same, valid signature

# Sends a GET request for this station to check if a user is currently logged in
def sendLoginCheck():
	url = conf.SERVER_URL + "/api/v1/checkuser/" + str(conf.STATION_ID)
	response = requests.get(url)
	userID = response.text
	#print(body["userID"])
	return userID


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

	signature = generateSignature(str(conf.STATION_ID) + "_" + str(tsMiddle) + "_" + str(random))
	url = conf.SERVER_URL + "/api/v1/video"
	print("[STORAGE] Making POST request to ", url, "...")
	payload = {
		"userID": userID,
		"stationID": conf.STATION_ID, 
		"timestamp": tsMiddle,
		"random": random,
		"hash_plain": signature[0],
		"hash": signature[1], # only for testing
		"signature": signature[2]
	}
	print(payload)
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

	uploadFile("rpi/vid/swingClip.mp4", "rpi/vid/swingClip.png", time.time(), True)
