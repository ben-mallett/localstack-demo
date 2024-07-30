import boto3
import os

def createDynamoDBTable():
    dynamodb = boto3.client(
        'dynamodb',
        endpoint_url=os.getenv('LOCALSTACK_URL'),
        region_name='us-east-1',
        aws_access_key_id='dummy',
        aws_secret_access_key='dummy'
    )
    try:
        dynamodb.create_table(
            TableName='Items',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        print("Table created successfully.")
    except dynamodb.exceptions.ResourceInUseException:
        print("Table already exists.")

def createS3Bucket():
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv('LOCALSTACK_URL'),
        region_name='us-east-1',
        aws_access_key_id='dummy',
        aws_secret_access_key='dummy'
    )
    bucketName = 'demo-bucket'
    try:
        s3.create_bucket(Bucket=bucketName)
        print("Bucket created successfully.")
    except s3.exceptions.BucketAlreadyExists:
        print("Bucket already exists.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print("Bucket already exists.")

if __name__ == "__main__":
    createDynamoDBTable()
    createS3Bucket()