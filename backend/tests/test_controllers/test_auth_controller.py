def test_register_user_success(client):
    
    # 1. Arrange: Define the JSON request payload (Like an incoming RequestDTO)
    registration_payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "SecurePassword123"
    }
    
    # 2. Act: Send a POST request (Like mockMvc.perform(post("/api/auth/register")))
    response = client.post("/api/auth/register", json=registration_payload)
    
    # 🛠️ MOCK DEBUGGER PRINT: This outputs the real error message to the terminal!
    print("\n--- [BACKEND RAW RESPONSE BODY] ---")
    print(response.json())
    print("-----------------------------------\n")

    # 3. Assert: Verify the response status and returned body (Like assertEquals / assertThat)
    assert response.status_code == 201  # We expect a 201 Created status[cite: 1]
    
    data = response.json()
    # assert data["username"] == "testuser"
    # assert data["email"] == "testuser@example.com"
    # assert "id" in data                 # Verify an database primary key ID was assigned