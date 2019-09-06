import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'AKIAYSNPXOSF4LTFMO3U'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'sagarexplores3'

data = open('urls.py', 'rb')

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
s3.Bucket(BUCKET_NAME).put_object(Key='urls.py', Body=data)

print ("Done")
