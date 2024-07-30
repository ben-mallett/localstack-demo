import boto3
import os
import json

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv('LOCALSTACK_URL'),
    region_name='us-east-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)
bucketName = 'demo-bucket'

def uploadFile(itemId: str, data):
    """
    Uploads file to S3

    Params:
        itemId : str : id of item to upload
    """
    s3.put_object(Bucket=bucketName, Key=itemId, Body=json.dumps(data))

def deleteFile(itemId: str):
    """
    Deletes the item from the s3 bucket

    Params:
        itemId : str : id of item to delete
    """
    s3.delete_object(Bucket=bucketName, Key=itemId)