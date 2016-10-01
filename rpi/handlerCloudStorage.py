# http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation

import boto3
from botocore.client import Config

# constants
BUCKET_NAME = "hopinone"

# connections
s3 = boto3.resource("s3", config=Config(signature_version='s3v4'))
bucket = s3.Bucket(BUCKET_NAME)




def uploadFile(fileName): 
	data = open(fileName, "rb")
	bucket.put_object(Key='test_ser10.mp4', Body=data, ACL="public-read")



if __name__ == '__main__':
	# Only executed if explicitely calling this file: use for testing purposes
	uploadFile("rpi/test/test_ser10.mp4")
