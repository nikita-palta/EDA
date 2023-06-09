import logging
import os

import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource("s3")
client = boto3.client('s3',
                      aws_access_key_id='',
                      aws_secret_access_key='')

class ed_aws_operations:
	'''Function to get all the buckets from S3'''
	def get_bucket_list(self):
		for bucket in s3.buckets.all():
			print(bucket.name)

	'''Function to upload a file to the given S3 bucket'''
	def upload_file_to_s3(self, bucket_name, file_name, object_name=None):
		# If S3 object_name was not specified, use file_name
		if object_name is None:
			object_name = os.path.basename(file_name)
		with open(file_name, "w") as f:
			f.writelines("This is a test file")
		try:
			response = client.upload_file(file_name, bucket_name, object_name)
		except ClientError as e:
			logging.error(e)
			return False
		return True


aws = ed_aws_operations()
