import pytest

@pytest.fixture
def user_token(client):
    """Helper fixture to register and log in a regular USER, returning their JWT access token."""
    user_payload = {
        "username": "carbuyer",
        "email": "buyer@dealership.com",
        "password": "SecurePassword123!"
    }
    client.post("/api/auth/register", json=user_payload)
    login_resp = client.post("/api/auth/login", json=user_payload)
    return login_resp.json()["access_token"]

def test_create_vehicle_success(client, user_token):
    """Happy Path: An authenticated user can successfully add a new vehicle to the inventory."""
    vehicle_payload = {
        "make": "Toyota",
        "model": "RAV4",
        "category": "SUV",
        "price": 32000.0,
        "quantity": 5
    }
    
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/api/vehicles", json=vehicle_payload, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["make"] == "Toyota"
    assert data["quantity"] == 5


def test_get_all_vehicles_success(client, user_token):
    """Happy Path: An authenticated user can successfully fetch the list of all available inventory items."""
    # Act: Send a GET request with our verified token format
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/api/vehicles", headers=headers)
    
    # Assert: Verify that the endpoint returns a valid array format
    assert response.status_code == 200
    assert isinstance(response.json(), list)
