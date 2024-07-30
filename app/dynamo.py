import boto3
import os

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv('LOCALSTACK_URL'),
    region_name='us-east-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)
table = dynamodb.Table('Items')

def getItem(itemId: str):
    """
    Gets an item from the dynamo instance

    Params:
        itemId : str : item ID to get
    
    Returns:
        item : Item : Item from database
    """
    response = table.get_item(Key={'id': itemId})
    return response.get('Item')

def putItem(itemId: str, data):
    """
    Puts an item in the dynamo instance

    Params:
        itemId : str : item ID to put
        data : Item : data to update with
    Returns:
        item : Item : Item from database
    """
    table.put_item(Item={'id': itemId, 'data': data})

def deleteItem(itemId: str):
    """
    Deletes an item in the dynamo instance

    Params:
        itemId : str : item ID to delete
    Returns:
        item : Item : Item from database
    """
    table.delete_item(Key={'id': itemId})