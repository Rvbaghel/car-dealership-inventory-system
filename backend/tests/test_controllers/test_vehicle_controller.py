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

def test_search_vehicles_by_make_success(client, user_token):
    """Happy Path: An authenticated user can successfully filter vehicles by query parameters."""
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # Arrange: Seed a vehicle explicitly into this isolated transaction context
    vehicle_payload = {
        "make": "Toyota",
        "model": "RAV4",
        "category": "SUV",
        "price": 32000.0,
        "quantity": 5
    }
    client.post("/api/vehicles", json=vehicle_payload, headers=headers)
    
    # Act: Request filtering for vehicles made by "Toyota"
    response = client.get("/api/vehicles/search?make=Toyota", headers=headers)
    
    # Assert: Verify response matrix format and correct filter application
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["make"] == "Toyota"


def test_update_vehicle_details_success(client, user_token):
    """Happy Path: An authenticated user can successfully update an existing vehicle's data details."""
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # Arrange: Seed an initial vehicle to obtain a persistent record ID
    initial_payload = {
        "make": "Honda",
        "model": "Civic",
        "category": "Sedan",
        "price": 25000.0,
        "quantity": 10
    }
    create_resp = client.post("/api/vehicles", json=initial_payload, headers=headers)
    vehicle_id = create_resp.json()["id"]

    # Act: Send the updated payload parameters via PUT
    update_payload = {
        "make": "Honda",
        "model": "Civic Hatchback",  # Changing the model
        "category": "Sedan",
        "price": 27000.0,            # Changing the price
        "quantity": 8                # Changing the stock quantity
    }
    response = client.put(f"/api/vehicles/{vehicle_id}", json=update_payload, headers=headers)
    
    # Assert: Verify database status and payload structural return update values
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == vehicle_id
    assert data["model"] == "Civic Hatchback"
    assert data["price"] == 27000.0
    assert data["quantity"] == 8   