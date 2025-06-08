from fastapi.testclient import TestClient
from Library.main import app
import uuid

client = TestClient(app)
email_librarian = f"admin+{uuid.uuid4().hex[:5]}@test.com"
email_reader = f"reader+{uuid.uuid4().hex[:5]}@test.com"

def test_cannot_borrow_fourth_book(client):
    register_resp = client.post("/users/register", json={
        "username": email_librarian,
        "password": "123456"
    })
    assert register_resp.status_code == 200

    login_resp = client.post("/users/login", data={
        "username": email_librarian,
        "password": "123456"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert login_resp.status_code == 200

    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    reader_resp = client.post("/readers/", json={
        "name": "Читатель",
        "email": email_reader,
        "password": "123456"
    }, headers=headers)

    assert reader_resp.status_code == 200
    reader_id = reader_resp.json()["id"]

    for i in range(3):
        book_resp = client.post("/books/", json={
            "title": f"Книга {i+1}",
            "author": "Автор К",
            "year": 2025,
            "num_of_books": 1
        }, headers=headers)
        assert book_resp.status_code == 200
        book_id = book_resp.json()["book_id"]

        borrow = client.post("/library/borrow", json={
            "book_id": book_id,
            "reader_id": reader_id
        }, headers=headers)
        assert borrow.status_code == 200

    book_4 = client.post("/books/", json={
        "title":"Чётвертая Книга",
        "author": "Я",
        "year": 2025,
        "num_of_books": 1
    }, headers=headers)
    assert book_4.status_code == 200
    book_4_id = book_4.json()["book_id"]

    borrow_4 = client.post("/library/borrow", json={
        "book_id": book_4_id,
        "reader_id": reader_id
    }, headers=headers)

    assert borrow_4.status_code == 400
    assert borrow_4.json()["detail"] == "Читатель уже имеет максимум книг (3шт.)"