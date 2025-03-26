from fastapi.testclient import TestClient

from api.security import get_password_hash
from tests.factories import UserFactory


def test_get_token(client: TestClient):
    user = UserFactory.create(password=get_password_hash("Test_password"))
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": "Test_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    response_keys = ["access_token", "refresh_token", "token_type"]
    response_json = response.json()

    assert response.status_code == 200
    for key in response_keys:
        assert key in response_json


def test_bad_login(client: TestClient):
    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "admin1"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
