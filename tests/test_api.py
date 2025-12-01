import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello api"}

def test_create_and_get_user():
    user_data = {"name": "Alice", "age": 22, "secret_name": "HeroA"}
    
    # إنشاء مستخدم
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert user["name"] == "Alice"
    
    user_id = user["id"]
    
    # جلب المستخدم
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["name"] == "Alice"

def test_update_user():
    user_data = {"name": "Bob", "age": 33, "secret_name": "HeroB"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]
    
    updated_data = {"name": "Bob Updated", "age": 34, "secret_name": "HeroB2"}
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Bob Updated"

def test_delete_user():
    user_data = {"name": "Charlie", "age": 40, "secret_name": "HeroC"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
