import pytest
from fastapi import status

def test_restock_vehicle_requires_authentication(client):
    """
    TDD Test 1 (RED): Enforces that the restock endpoint cannot be accessed 
    without a valid structural Authorization header.
    """
    vehicle_id = 1
    restock_payload = {"quantity": 5}
    
    # Path A: Missing Authorization Header entirely
    response_missing = client.post(f"/api/vehicles/{vehicle_id}/restock", json=restock_payload)
    assert response_missing.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_missing.json()["detail"] == "Missing or invalid Authorization header structural format"
    
    # Path B: Invalid structural format (Missing 'Bearer ' prefix)
    bad_headers = {"Authorization": "NotABearerToken12345"}
    response_bad_format = client.post(
        f"/api/vehicles/{vehicle_id}/restock", 
        json=restock_payload, 
        headers=bad_headers
    )
    assert response_bad_format.status_code == status.HTTP_401_UNAUTHORIZED

def test_restock_vehicle_success_increases_quantity_as_admin(admin_client, test_db_vehicle):
    """
    TDD Test 2 (RED): Enforces that an authenticated ADMIN can successfully 
    restock a vehicle, incrementing its stock quantity in the database.
    """
    vehicle_id = test_db_vehicle.id
    # Let's say starting quantity is 8 (based on our previous DB items)
    initial_quantity = test_db_vehicle.quantity 
    restock_payload = {"quantity": 5}
    
    # We use admin_client which automatically provides a valid ADMIN token
    response = admin_client.post(f"/api/vehicles/{vehicle_id}/restock", json=restock_payload)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify the stock increments accurately in the returned JSON state
    assert data["quantity"] == initial_quantity + 5    