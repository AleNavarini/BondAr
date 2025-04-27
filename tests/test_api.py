from fastapi.testclient import TestClient
from src.__main__ import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "App is running", "status": "OK"}

def test_bond_endpoint_success(mock_google_client, sample_bond_data):
    # Test with a valid bond symbol
    response = client.get("/bond/BONAR24")
    assert response.status_code == 200
    data = response.json()
    assert data["simbolo"] == "BONAR24"
    assert data["precio"] == 100.5
    assert data["tasa"] == 0.05

def test_bond_endpoint_not_found(mock_google_client):
    # Test with a non-existent bond symbol
    response = client.get("/bond/NONEXISTENT")
    assert response.status_code == 200  # Since we return 200 with error message
    assert response.json() == {"message": "Symbol not found", "status": "ERROR"}

def test_bond_endpoint_with_asterisk(mock_google_client, sample_bond_data):
    # Test that asterisks are properly handled
    response = client.get("/bond/BONAR24*")
    assert response.status_code == 200
    data = response.json()
    assert data["simbolo"] == "BONAR24"
    assert data["precio"] == 100.5 