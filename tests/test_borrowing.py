from fastapi.testclient import TestClient
from Library.main import app
import uuid

client = TestClient(app)
email = f"admin+{uuid.uuid4().hex[:5]}@test.com"

def test_cannot_borrow_unavailable_book(client):
    register_response = client.post("/users/register", json={
        "username": email,
        "password": "123456"
    })
    assert register_response.status_code == 200

    login_response = client.post("/users/login", data={
        "username": email,
        "password": "123456"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    reader_resp = client.post("/readers/", json={
        "name": "Тест читатель",
        "email": "reader@test.com",
        "password": "123456"
    }, headers=headers)
    assert reader_resp.status_code == 200
    reader_id = reader_resp.json()["id"]

    book_resp = client.post("/books/", json={
        "title": "Тест книга",
        "author": "КОхай",
        "year": 2025,
        "num_of_books": 1
    }, headers=headers)
    assert book_resp.status_code == 200
    book_id = book_resp.json()["book_id"]

    borrow_1 = client.post("/library/borrow", json={
        "book_id": book_id,
        "reader_id": reader_id
    }, headers=headers)
    assert borrow_1.status_code == 200

    borrow_2 = client.post("/library/borrow", json={
        "book_id": book_id,
        "reader_id": reader_id
    }, headers=headers)
    assert borrow_2.status_code == 400
    assert borrow_2.json()["detail"] == "Нет доступных экземпляров книги"