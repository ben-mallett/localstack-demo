from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dynamo import getItem, putItem, deleteItem
from s3 import uploadFile, deleteFile

app = FastAPI()

class Item(BaseModel):
    id: str
    data: dict

@app.get('/')
async def root():
    """
    Simple route for testing purposes.
    """
    return 'hello world'

@app.get("/items/{itemId}")
async def readItem(itemId: str):
    """
    Reads an item from the Dynamo instance. If an item does not exist, raises a 404

    Params:
        itemId : str : id of item to get
    Returns: 
        item : Item : item from db
    Raises:
        HTTPException : 404 : If item is not found raises 404
    """
    item = getItem(itemId)
    if item:
        return item
    else: 
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/")
async def createItem(item: Item):
    """
    Creates an item and puts it in the S3 bucket and dynamo instance. If an item exists already raises an exception

    Params:
        itemId : str : id of item to create
    Returns: 
        item : Item : item after creation
    Raises:
        HTTPException : 404 : If item already exists raises 404
    """
    if getItem(item.id):
        raise HTTPException(status_code=400, detail="Item already exists")
    try:
        putItem(item.id, item.data)
        uploadFile(item.id, item.data)
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error in processing:\n {e}')


@app.put("/items/{itemId}")
async def updateItemEndpoint(itemId: str, item: Item):
    """
    Updates an item in both dynamo and s3 instances. If an item does not exist, raises a 404

    Params:
        itemId : str : id of item to get
        item : Item : updated item data
    Returns: 
        item : Item : item from db
    Raises:
        HTTPException : 404 : If item is not found raises 404
    """
    if not getItem(itemId):
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        putItem(itemId, item.data)
        uploadFile(itemId, item.data)
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error in processing:\n {e}')


@app.delete("/items/{itemId}")
async def deleteItemEndpoint(itemId: str):
    """
    Deletes an item from both dynamo and s3 instances. If an item does not exist, raises a 404

    Params:
        itemId : str : id of item to delete
    Returns: 
        message : JSON : message with deleted item
    Raises:
        HTTPException : 404 : If item is not found raises 404
    """
    if not getItem(itemId):
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        deleteItem(itemId)
        deleteFile(itemId)
        return {"message": "Item deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error in processing:\n {e}')

