import pytest

def test_register_user_success(client):
    """Happy Path: Standard registration workflow should return 201 Created."""
    registration_payload = {
        "username": "happyuser",
        "email": "happyuser@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/auth/register", json=registration_payload)
    assert response.status_code == 201
    assert response.json()["username"] == "happyuser"

def test_register_duplicate_username_fails(client):
    """Business Constraint Rule: Registering an existing username must return 400 Bad Request."""
    payload = {
        "username": "duplicateuser",
        "email": "user1@example.com",
        "password": "Password123!"
    }
    # First registration passes
    client.post("/api/auth/register", json=payload)
    
    # Second registration with identical username fails
    payload["email"] = "user2@example.com"
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

def test_register_invalid_email_fails(client):
    """Structural Schema Validation: Invalid email string formats must return 422 Unprocessable Entity."""
    payload = {
        "username": "emailtest",
        "email": "invalid-email-format",
        "password": "Password123!"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 422

def test_register_weak_password_fails(client):
    """Structural Schema Validation: Password missing criteria (min-length 6, upper, lower, digit, special) must return 422."""
    bad_passwords = [
        "short",          # Length under 6 characters
        "nocapital123!",  # Missing uppercase letter
        "NOLOWERCASE1!",  # Missing lowercase letter
        "NoSpecialChar1", # Missing special character
        "NoDigitsLetters!" # Missing numeric digit
    ]
    
    for password in bad_passwords:
        payload = {
            "username": f"user_{password[:4]}",
            "email": f"test_{password[:4]}@example.com",
            "password": password
        }
        response = client.post("/api/auth/register", json=payload)
        assert response.status_code == 422, f"Failed to catch weak password: {password}"

#login features 
def test_login_user_success(client):
    """Happy Path: Submitting valid credentials must return 200 OK and user details."""
    # 1. Arrange: Register a user first
    setup_payload = {
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "SecurePassword123!"
    }
    client.post("/api/auth/register", json=setup_payload)

    # 2. Act: Attempt login with correct credentials
    login_payload = {
        "email": "logintest@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/auth/login", json=login_payload)

    # 3. Assert: Verify the response matches our design contract
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["username"] == "logintest"

def test_login_invalid_password_fails(client):
    """Security Failure: Submitting a wrong password must return 401 Unauthorized."""
    # 1. Arrange: Register a user
    setup_payload = {
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "SecurePassword123!"
    }
    client.post("/api/auth/register", json=setup_payload)

    # 2. Act: Login with an incorrect password
    bad_login_payload = {
        "email": "wrongpass@example.com",
        "password": "WrongPassword123!"
    }
    response = client.post("/api/auth/login", json=bad_login_payload)

    # 3. Assert: Expect a clear authentication failure response
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_login_nonexistent_user_fails(client):
    """Security Failure: Attempting to login an email that doesn't exist must return 401."""
    login_payload = {
        "email": "nobody@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"