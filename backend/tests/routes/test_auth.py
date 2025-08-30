import pytest


@pytest.mark.asyncio
async def test_register_endpoint_success(client):
    user_data = {"email": "test@example.com", "password": "testpassword"}
    response = await client.post("auth/register", json=user_data)

    assert response.status_code == 201
    assert response.json()["user"]["email"] == user_data["email"]
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_endpoint_user_exists(client):
    user_data = {"email": "test@example.com", "password": "testpassword"}
    await client.post("/register", json=user_data)

    response = await client.post("auth/register", json=user_data)

    assert response.status_code == 400
    assert "User already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_endpoint_success(client):
    user_data = {"email": "test@example.com", "password": "testpassword"}
    await client.post("/register", json=user_data)

    response = await client.post("auth/login", json=user_data)

    assert response.status_code == 200
    assert response.json()["user"]["email"] == user_data["email"]
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_endpoint_invalid_credentials(client):
    user_data = {"email": "test@example.com", "password": "wrongpassword"}
    response = await client.post("auth/login", json=user_data)

    assert response.status_code == 400
    assert "Invalid credentials" in response.json()["detail"]
