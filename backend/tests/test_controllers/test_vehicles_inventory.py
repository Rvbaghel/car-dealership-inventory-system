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