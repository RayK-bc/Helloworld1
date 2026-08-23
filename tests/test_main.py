from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Performance Demo"}

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_read_item_valid():
    response = client.get("/api/v1/items/42")
    assert response.status_code == 200
    assert response.json()["item_id"] == 42

def test_read_item_invalid():
    response = client.get("/api/v1/items/0")
    assert response.status_code == 400