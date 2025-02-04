from fastapi.testclient import TestClient
from numberApi import app

client = TestClient(app)

def test_valid_number():
    response = client.get("/api/classify-number?number=371")
    assert response.status_code == 200
    assert response.json()["number"] == 371
    assert "armstrong" in response.json()["properties"]

def test_negative_number():
    response = client.get("/api/classify-number?number=-5")
    assert response.status_code == 400

def test_invalid_input():
    response = client.get("/api/classify-number?number=abc")
    assert response.status_code == 422  # Expect 422, not 400
