from fastapi.testclient import TestClient
from Library.main import app
import uuid

client = TestClient(app)

def test_access_protected_endpoint(client):
    email = f"admin+{uuid.uuid4().hex[:5]}@test.com"

    register_resp = client.post("/users/register", json={
        "username": email,
        "password": "123456"
    })
    assert register_resp.status_code == 200

    login_resp = client.post("/users/login", data={
        "username": email,
        "password": "123456"
    })
    assert login_resp.status_code == 200

    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    with_token = client.post("/books/", json={
        "title": "Тест Книга",
        "author": "Кирилл В.",
        "year": 1997,
        "num_of_books": 1
    }, headers=headers)
    assert with_token.status_code == 200

    without_token = client.post("/books/", json={
        "title":"Без Токена",
        "author":"Нельзя",
        "year": 2026,
        "num_of_books": 1
    })
    assert without_token.status_code == 401

