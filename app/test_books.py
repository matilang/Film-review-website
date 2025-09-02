from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_book():
    response = client.post(
        "/books/",
        json={"title" : "Moja ksiazka", "author" : "No ja", "year" : 2025} 
    )
    book_id = response.json()['id']

    assert response.status_code == 201
    assert response.json() == {
        "title" : "Moja ksiazka",
        "author" : "No ja",
        "year" : 2025,
        "id" : book_id
    }
