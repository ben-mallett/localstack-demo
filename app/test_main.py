from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'hello world'

def test_create_item():
    response = client.post("/items/", json={"id": "test1", "data": {"key": "value"}})
    assert response.status_code == 200
    assert response.json() == {"id": "test1", "data": {"key": "value"}}

def test_create_with_conflict():
    client.post("/items/", json={"id": "test2", "data": {"key": "value"}})
    response = client.post("/items/", json={"id": "test2", "data": {"key": "value"}})
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}

def test_get_item():
    client.post("/items/", json={"id": "test3", "data": {"key": "value"}})
    response = client.get("/items/test3")
    assert response.status_code == 200
    assert response.json() == {"id": "test3", "data": {"key": "value"}}

def test_get_nonexistent_item():
    response = client.get("/items/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_get_item_empty():
    client.post("/items/", json={"id": "test4", "data": {}})
    response = client.get("/items/test4")
    assert response.status_code == 200
    assert response.json() == {"id": "test4", "data": {}}

def test_put_item():
    client.post("/items/", json={"id": "test5", "data": {"key": "value"}})
    response = client.put("/items/test5", json={"id": "test5", "data": {"key": "new_value"}})
    print(response.json())

    assert response.status_code == 200
    assert response.json() == {"id": "test5", "data": {"key": "new_value"}}

def test_put_item_without_target():
    response = client.put("/items/nonexistent", json={"id": "nonexistent", "data": {"key": "value"}})
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_delete_item():
    client.post("/items/", json={"id": "test6", "data": {"key": "value"}})
    response = client.delete("/items/test6")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}

def test_delete_nonexistent_item():
    response = client.delete("/items/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
