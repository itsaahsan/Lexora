def test_register(client):
    response = client.post("/api/auth/register", json={
        "email": "new@example.com",
        "password": "password123",
        "full_name": "New User",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["user"]["email"] == "new@example.com"


def test_register_duplicate(client, test_user):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
    })
    assert response.status_code == 400


def test_login(client, test_user):
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword",
    })
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_invalid(client):
    response = client.post("/api/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_get_me(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_get_me_unauthorized(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
