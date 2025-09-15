import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from app.main import app
from app.dependencies import get_session


TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


#fixture creating SQL Base
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


#fixture creating FastAPI client
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()

#fixture creating sample book
@pytest.fixture
def sample_book(client):
    response = client.post("/books/", json = {
        "title" : "Book A", "author" : "Author A", "year" : 2000
    })
    return response.json()

@pytest.fixture
def sample_list_of_books(client):
    books = []
    for data in [
        {"title": "Book A", "author": "Author A", "year": 2000},
        {"title": "Book B", "author": "Author B", "year": 1992},
        {"title": "Book C", "author": "Author C", "year": 2010},
    ]:
        response = client.post("/books/", json=data)
        books.append(response.json())

    return books

@pytest.fixture
def sample_list_of_reviews(client, sample_book):
    book_id = sample_book['id']
    review_text = "Review test content"
    reviews = []
    
    for data in [
        {"book_id": book_id, "review_text": review_text, "rating": 2.3},
        {"book_id": book_id, "review_text": review_text, "rating": 5},
        {"book_id": book_id, "review_text": review_text, "rating": 4.33},
    ]:

        response = client.post(f"/books/{book_id}/reviews/", json = data)
        reviews.append(response.json())
    
    return reviews
    