import pytest
from httpx import AsyncClient
from app.main import app  # Ensure this imports your FastAPI application correctly

@pytest.mark.asyncio
async def test_retrieve_access_token():
    credentials = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        token_resp = await client.post("/token", data=credentials)
    assert token_resp.status_code == 200
    assert "access_token" in token_resp.json()
    assert token_resp.json().get("token_type") == "bearer"

@pytest.mark.asyncio
async def test_unauthenticated_qr_request():
    qr_data = {
        "target_url": "https://amazon.com",
        "primary_color": "blue",
        "background_color": "green",
        "dimensions": 12,
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/qr-codes/", json=qr_data)
    assert response.status_code == 401  # Expecting Unauthorized status

@pytest.mark.asyncio
async def test_authenticated_qr_operations():
    credentials = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        auth_response = await client.post("/token", data=credentials)
        valid_token = auth_response.json()["access_token"]
        authorization_header = {"Authorization": f"Bearer {valid_token}"}

        qr_creation_data = {
            "target_url": "https://amazon.com",
            "primary_color": "blue",
            "background_color": "green",
            "dimensions": 12,
        }
        qr_creation_response = await client.post("/qr-codes/", json=qr_creation_data, headers=authorization_header)
        assert qr_creation_response.status_code in [201, 409]

        if qr_creation_response.status_code == 201:
            qr_resource_link = qr_creation_response.json()["qr_code_url"]
            qr_file_identifier = qr_resource_link.split('/')[-1]
            qr_deletion_response = await client.delete(f"/qr-codes/{qr_file_identifier}", headers=authorization_header)
            assert qr_deletion_response.status_code == 204
