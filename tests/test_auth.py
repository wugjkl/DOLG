def test_register_and_login(client):
    # 1. Register User
    reg_response = client.post(
        "/auth/register",
        json={"email": "alice@example.com", "name": "Alice", "password": "secretpassword"}
    )
    assert reg_response.status_code == 201
    data = reg_response.json()
    assert data["email"] == "alice@example.com"
    assert data["name"] == "Alice"
    assert "id" in data

    # 2. Login User
    login_response = client.post(
        "/auth/json-login",
        json={"email": "alice@example.com", "password": "secretpassword"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 3. Get Profile (/auth/me)
    profile_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "alice@example.com"


def test_duplicate_registration_fails(client):
    client.post("/auth/register", json={"email": "bob@example.com", "name": "Bob", "password": "pass"})
    response = client.post("/auth/register", json={"email": "bob@example.com", "name": "Bob", "password": "pass"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]
