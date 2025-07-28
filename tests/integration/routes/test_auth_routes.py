import pytest


@pytest.mark.integration
def test_register_user(client):
    """Test Register auth route."""

    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.integration
def test_register_user_with_exists(client):
    """Test Register auth route."""

    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "full_name": "Test User",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "full_name": "Test User 2",
        },
    )
    assert response.status_code == 400


@pytest.mark.integration
def test_login_user(client):
    """Test Login auth route."""

    client.post(
        "/auth/register",
        json={
            "email": "test2@example.com",
            "password": "123456",
            "full_name": "Test User",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test2@example.com",
            "password": "123456",
        },
    )

    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data


@pytest.mark.integration
def test_invalid_credentials_user(client):
    """Test Login with bad credentials"""

    response = client.post(
        "/auth/login",
        json={
            "email": "bad_email@21-942",
            "password": "4567",
            "full_name": "bad Test User",
        },
    )

    assert response.status_code == 400
